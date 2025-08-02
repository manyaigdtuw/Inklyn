import streamlit as st
import openai
from datetime import datetime
import json
import uuid
from doc_processor import DocumentProcessor
from ai_engine import AIEngine
from email_assistant import EmailAssistant
from config import Config
from streamlit_option_menu import option_menu
import extra_streamlit_components as stx

# Configure page
st.set_page_config(
    page_title=Config.PAGE_TITLE,
    page_icon=Config.PAGE_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize components
@st.cache_resource
def init_components():
    return {
        'doc_processor': DocumentProcessor(),
        'ai_engine': AIEngine(),
        'email_assistant': EmailAssistant()
    }

components = init_components()

# Initialize session state
def init_session_state():
    if 'session_id' not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'uploaded_files' not in st.session_state:
        st.session_state.uploaded_files = []
    if 'file_contents' not in st.session_state:
        st.session_state.file_contents = {}
    if 'current_context' not in st.session_state:
        st.session_state.current_context = ""
    if 'selected_model' not in st.session_state:
        st.session_state.selected_model = Config.DEFAULT_MODEL

init_session_state()

# Custom CSS
def load_css():
    st.markdown("""
    <style>
    .main {
        padding-top: 1rem;
    }
    
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    
    .assistant-message {
        background-color: #f5f5f5;
        border-left: 4px solid #4caf50;
    }
    
    .file-info {
        background-color: #fff3e0;
        padding: 10px;
        border-radius: 5px;
        border-left: 4px solid #ff9800;
        margin: 10px 0;
    }
    
    .success-message {
        background-color: #e8f5e8;
        color: #2e7d32;
        padding: 10px;
        border-radius: 5px;
        border-left: 4px solid #4caf50;
    }
    
    .error-message {
        background-color: #ffebee;
        color: #c62828;
        padding: 10px;
        border-radius: 5px;
        border-left: 4px solid #f44336;
    }
    
    .stButton > button {
        width: 100%;
        border-radius: 20px;
        border: none;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    .stTextInput > div > div > input {
        border-radius: 20px;
    }
    
    .model-selector {
        padding: 10px;
        background: #f0f0f0;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

load_css()

# Main App Layout
def main():
    st.title("Inklyn")
    st.markdown("**Upload any file and I'll help you understand it, write emails, or answer questions!**")
    
    # Sidebar for file management and settings
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # Model selection
        st.markdown('<div class="model-selector">', unsafe_allow_html=True)
        st.subheader("🧠 AI Model")
        available_models = components['ai_engine'].get_available_models()
        
        selected_model_name = st.selectbox(
            "Choose AI Model:",
            list(available_models.keys()),
            index=list(available_models.values()).index(st.session_state.selected_model)
        )
        
        if available_models[selected_model_name] != st.session_state.selected_model:
            st.session_state.selected_model = available_models[selected_model_name]
            components['ai_engine'].change_model(st.session_state.selected_model)
            st.success(f"Switched to {selected_model_name}")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.header(" File Manager")
        
        # File upload
        uploaded_files = st.file_uploader(
            "Upload Documents",
            type=Config.SUPPORTED_FORMATS,
            accept_multiple_files=True,
            help="Supported: PDF, Word, Excel, Images, PowerPoint, and more!"
        )
        
        # Process uploaded files
        if uploaded_files:
            process_uploaded_files(uploaded_files)
        
        # Display current files
        display_current_files()
        
        # Quick actions
        st.subheader("⚡ Quick Actions")
        if st.button("📝 Help me write an email"):
            st.session_state.quick_action = "write_email"
        if st.button("📧 Help me reply to an email"):
            st.session_state.quick_action = "reply_email"
        if st.button("📊 Analyze my documents"):
            st.session_state.quick_action = "analyze_docs"
        if st.button("🔄 Clear conversation"):
            clear_conversation()
    
    # Main chat interface
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Chat history
        display_chat_history()
    
    with col2:
        # Context panel
        display_context_panel()
    
    # IMPORTANT: Chat input must be at main level, not inside columns!
    handle_chat_input()

def process_uploaded_files(uploaded_files):
    """Process and store uploaded files"""
    for uploaded_file in uploaded_files:
        if uploaded_file.name not in [f['name'] for f in st.session_state.uploaded_files]:
            with st.spinner(f"Processing {uploaded_file.name}..."):
                try:
                    # Save file temporarily
                    file_content = uploaded_file.read()
                    
                    # Process with document processor
                    result = components['doc_processor'].process_file(
                        file_content, uploaded_file.name, uploaded_file.type
                    )
                    
                    if result['success']:
                        # Store file info
                        file_info = {
                            'name': uploaded_file.name,
                            'type': uploaded_file.type,
                            'size': len(file_content),
                            'content': result['content'],
                            'metadata': result['metadata'],
                            'processed_at': datetime.now().strftime("%Y-%m-%d %H:%M")
                        }
                        
                        st.session_state.uploaded_files.append(file_info)
                        st.session_state.file_contents[uploaded_file.name] = result['content']
                        
                        # Update context
                        update_context()
                        
                        st.success(f"✅ Successfully processed {uploaded_file.name}")
                    else:
                        st.error(f"❌ Error processing {uploaded_file.name}: {result['error']}")
                        
                except Exception as e:
                    st.error(f"❌ Error processing {uploaded_file.name}: {str(e)}")

def display_current_files():
    """Display currently uploaded files"""
    if st.session_state.uploaded_files:
        st.subheader("Current Files")
        for i, file_info in enumerate(st.session_state.uploaded_files):
            with st.expander(f"{file_info['name']}", expanded=False):
                st.markdown(f"**Type:** {file_info['type']}")
                st.markdown(f"**Size:** {file_info['size']:,} bytes")
                st.markdown(f"**Processed:** {file_info['processed_at']}")
                
                # Show content preview
                content_preview = file_info['content'][:300] + "..." if len(file_info['content']) > 300 else file_info['content']
                st.text_area("Content Preview", content_preview, height=100, disabled=True)
                
                # Remove file option
                if st.button(f"🗑️ Remove", key=f"remove_{i}"):
                    st.session_state.uploaded_files.pop(i)
                    del st.session_state.file_contents[file_info['name']]
                    update_context()
                    st.rerun()

def display_chat_history():
    """Display chat conversation"""
    if st.session_state.chat_history:
        for message in st.session_state.chat_history:
            if message['role'] == 'user':
                st.markdown(f"""
                <div class="chat-message user-message">
                    <strong>You:</strong><br>
                    {message['content']}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-message assistant-message">
                    <strong>AI Assistant:</strong><br>
                    {message['content']}
                </div>
                """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-message assistant-message">
            <strong>AI Assistant ({st.session_state.selected_model}):</strong><br>
            Hello! I'm your AI Document Assistant powered by OpenRouter. Upload any files and I can help you:
            <ul>
                <li>Understand and explain document content</li>
                <li>Write professional emails</li>
                <li>Reply to emails with context</li>
                <li>Analyze data and documents</li>
                <li> Answer questions about your files</li>
            </ul>
            How can I assist you today?
        </div>
        """, unsafe_allow_html=True)

def handle_chat_input():
    """Handle user chat input - MUST be at main level"""
    # Check for quick actions first
    if 'quick_action' in st.session_state:
        handle_quick_action(st.session_state.quick_action)
        del st.session_state.quick_action
        st.rerun()
    
    # Chat input - THIS MUST BE AT MAIN LEVEL, NOT IN COLUMNS
    user_input = st.chat_input("Type your message here...")
    
    if user_input:
        # Add user message to history
        st.session_state.chat_history.append({
            'role': 'user',
            'content': user_input,
            'timestamp': datetime.now()
        })
        
        # Get AI response
        with st.spinner("Thinking..."):
            ai_response = components['ai_engine'].generate_response(
                user_input,
                st.session_state.current_context,
                st.session_state.chat_history
            )
        
        # Add AI response to history
        st.session_state.chat_history.append({
            'role': 'assistant',
            'content': ai_response,
            'timestamp': datetime.now()
        })
        
        st.rerun()

def handle_quick_action(action):
    """Handle quick action buttons"""
    if action == "write_email":
        st.session_state.chat_history.append({
            'role': 'user',
            'content': "Help me write a professional email using the context from my uploaded files.",
            'timestamp': datetime.now()
        })
    elif action == "reply_email":
        st.session_state.chat_history.append({
            'role': 'user',
            'content': "Help me reply to an email. I'll provide the original email content.",
            'timestamp': datetime.now()
        })
    elif action == "analyze_docs":
        st.session_state.chat_history.append({
            'role': 'user',
            'content': "Please analyze all my uploaded documents and provide a comprehensive summary.",
            'timestamp': datetime.now()
        })

def display_context_panel():
    """Display context and file information panel"""
    st.subheader("🎯 Current Context")
    
    # Model info
    st.info(f"🧠 Using: {st.session_state.selected_model}")
    
    if st.session_state.uploaded_files:
        st.markdown(f"**Files:** {len(st.session_state.uploaded_files)} documents loaded")
        
        # Context summary
        if st.session_state.current_context:
            with st.expander("📝 Context Summary", expanded=True):
                st.text_area(
                    "Current understanding:",
                    st.session_state.current_context[:500] + "..." if len(st.session_state.current_context) > 500 else st.session_state.current_context,
                    height=200,
                    disabled=True
                )
    else:
        st.info("No files uploaded yet. Upload documents to get started!")
    
    

def update_context():
    """Update current context based on uploaded files"""
    if st.session_state.uploaded_files:
        context_parts = []
        for file_info in st.session_state.uploaded_files:
            context_parts.append(f"File: {file_info['name']}\nContent: {file_info['content'][:1000]}")
        
        st.session_state.current_context = "\n\n".join(context_parts)

def clear_conversation():
    """Clear chat history"""
    st.session_state.chat_history = []
    st.session_state.uploaded_files = []
    st.session_state.file_contents = {}
    st.session_state.current_context = ""
    st.success("🔄 Conversation cleared!")
    st.rerun()

if __name__ == "__main__":
    # Check if OpenRouter API key is configured
    if not Config.OPENROUTER_API_KEY:
        st.error("🚨 OpenRouter API key not configured!")
        st.markdown("""
        Please add your OpenRouter API key to the `.env` file:
        1. Go to [OpenRouter.ai](https://openrouter.ai) and get your API key
        2. Add it to `.env` file: `OPENROUTER_API_KEY=your_key_here`
        3. Restart the application
        """)
        st.stop()
    
    main()
