import httpx
import json
from config import Config
import streamlit as st

class AIEngine:
    def __init__(self):
        self.api_key = Config.OPENROUTER_API_KEY
        self.base_url = Config.OPENROUTER_BASE_URL
        self.app_name = Config.APP_NAME
        self.model = Config.DEFAULT_MODEL
        
        if not self.api_key:
            st.error("⚠️ OpenRouter API key not found! Please add it to your .env file")
    
    def generate_response(self, user_message, context, chat_history):
        """Generate AI response using OpenRouter"""
        try:
            # Build conversation context
            messages = self._build_messages(user_message, context, chat_history)
            
            # Make API call to OpenRouter
            response = self._call_openrouter_api(messages)
            
            return response
            
        except Exception as e:
            return f"I apologize, but I encountered an error: {str(e)}. Please try again."
    
    def _build_messages(self, user_message, context, chat_history):
        """Build message array for API call"""
        messages = []
        
        # System prompt
        system_prompt = f"""You are an AI Document Assistant that helps users understand documents, write emails, and answer questions.

Current Context from uploaded files:
{context}

You can help with:
1. 📖 Explaining document content
2. 📝 Writing professional emails
3. 📧 Replying to emails with context
4. 📊 Analyzing data and documents  
5. ❓ Answering questions about uploaded files

Be helpful, professional, and use the document context when relevant."""

        messages.append({"role": "system", "content": system_prompt})
        
        # Add recent chat history (last 10 messages)
        recent_history = chat_history[-10:] if len(chat_history) > 10 else chat_history
        for msg in recent_history:
            if msg['role'] in ['user', 'assistant']:
                messages.append({
                    "role": msg['role'],
                    "content": msg['content']
                })
        
        return messages
    
    def _call_openrouter_api(self, messages):
        """Make API call to OpenRouter"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": "http://localhost:8501",  # Streamlit default
            "X-Title": self.app_name,
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model,
            "messages": messages,
            "max_tokens": Config.MAX_TOKENS,
            "temperature": Config.TEMPERATURE,
            "stream": False
        }
        
        with httpx.Client(timeout=30.0) as client:
            response = client.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=data
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content'].strip()
            else:
                error_msg = f"API Error {response.status_code}: {response.text}"
                st.error(error_msg)
                return "I'm having trouble connecting to the AI service. Please try again."
    
    def change_model(self, model_name):
        """Change the AI model"""
        if model_name in Config.AVAILABLE_MODELS.values():
            self.model = model_name
            return True
        return False
    
    def get_available_models(self):
        """Get list of available models"""
        return Config.AVAILABLE_MODELS
