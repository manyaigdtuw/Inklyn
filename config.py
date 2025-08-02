import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    
    OPENROUTER_API_KEY = os.environ.get('OPENROUTER_API_KEY')
    OPENROUTER_BASE_URL = os.environ.get('OPENROUTER_BASE_URL', 'https://openrouter.ai/api/v1')
    APP_NAME = os.environ.get('APP_NAME', 'AI Document Chatbot')
    
    # Model settings
    DEFAULT_MODEL = os.environ.get('DEFAULT_MODEL', 'anthropic/claude-3-haiku')
    MAX_TOKENS = 2000
    TEMPERATURE = 0.7
    
    # File settings
    MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
    SUPPORTED_FORMATS = [
        'pdf', 'docx', 'doc', 'txt', 'csv', 'xlsx', 'xls',
        'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'webp',
        'pptx', 'json', 'html', 'md', 'rtf'
    ]
    
    # UI settings
    PAGE_TITLE = "inklyn<3"
    PAGE_ICON = "❤️"
    
    # Available models (you can add more)
    AVAILABLE_MODELS = {
        'Claude 3 Haiku': 'anthropic/claude-3-haiku',
        'Claude 3 Sonnet': 'anthropic/claude-3-sonnet',
        'GPT-4 Turbo': 'openai/gpt-4-turbo-preview',
        'GPT-3.5 Turbo': 'openai/gpt-3.5-turbo',
        'Llama 2 70B': 'meta-llama/llama-2-70b-chat',
        'Gemini Pro': 'google/gemini-pro'
    }
