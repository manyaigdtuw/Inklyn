# Inklyn

AI-powered document assistant that helps users understand documents, write emails, and answer questions based on uploaded files. Built with Streamlit and integrated with OpenRouter API for advanced AI responses.

## Features

- Upload and process various document types: PDF, DOCX, TXT, CSV, Excel, PPTX, JSON, images with OCR, and more.
- Extract text, analyze data, and summarize content.
- Ask questions about uploaded documents.
- Compose and reply to professional emails using AI.
- Supports multiple AI models accessible via OpenRouter.
- User-friendly web interface with session management and chat history.


## Installation

### Prerequisites

- Python 3.8 or higher
- Tesseract OCR installed and configured (required for image OCR functionality). See: https://github.com/tesseract-ocr/tesseract
- An OpenRouter API key (free or paid, obtain from OpenRouter platform)

### Setup

1. Clone the repository:
   - git clone https://github.com/manyaigdtuw/Inklyn
   - cd Inklyn

2. (Optional) Use the provided setup script to scaffold the environment and files:
    python setup_project.py


3. Install dependencies:
   pip install -r requirements.txt


4. Create a `.env` file in the root directory with your OpenRouter API key and app settings:
  -  OPENROUTER_API_KEY=your_openrouter_api_key_here
  - OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
  - APP_NAME=AI Document Chatbot
  - DEFAULT_MODEL=anthropic/claude-3-haiku

5. Run the application:
   streamlit run app.py


## Usage

- Upload files via the Streamlit UI.
- The app automatically processes and extracts content from uploaded files.
- Chat with the AI assistant to get document explanations, summaries, or draft emails.
- Select different AI models from the sidebar as needed.

## Project Structure

- `app.py` — Main Streamlit application.
- `ai_engine.py` — Interacts with OpenRouter API for AI-generated responses.
- `document_processor.py` — Processes uploaded documents (PDF, Word, images, spreadsheets, etc.) with OCR support.
- `email_assistant.py` — AI-powered email writing and replying helper.
- `config.py` — Configuration and environment variables.
- `requirements.txt` — Python dependencies.
- `setup_project.py` — Automated project setup script.

## Supported File Types

- PDF, Word (`.docx`, `.doc`), Text, CSV, Excel, PowerPoint, JSON.
- Images: PNG, JPG, BMP, TIFF, WebP (with OCR extraction).
- Generic text for unrecognized file formats.

## Technologies Used

- [Streamlit](https://streamlit.io) — Web app framework.
- [OpenRouter API](https://openrouter.ai) — AI language model API.
- [PyMuPDF](https://pymupdf.readthedocs.io/) — PDF parsing.
- [python-docx](https://python-docx.readthedocs.io/) — Word document parsing.
- [Pandas](https://pandas.pydata.org) — Data analysis and processing.
- [Pillow](https://python-pillow.org) — Image processing.
- [PyTesseract](https://github.com/madmaze/pytesseract) & [EasyOCR](https://github.com/JaidedAI/EasyOCR) — Optical character recognition (OCR).
- [python-pptx](https://python-pptx.readthedocs.io/) — PowerPoint file processing.

## Contributing

Contributions are welcome! Please open issues or submit pull requests for improvements and fixes.


## Acknowledgements

- Thanks to OpenRouter for providing AI APIs.
- Inspired by open-source projects for document processing and AI chatbots.



