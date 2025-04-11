# AI as Enabler - LinkedIn Post Generator

This application generates LinkedIn posts based on article content, focusing on the "AI as enabler" philosophy. The application is split into two components:

1. **FastAPI Backend**: Handles the business logic, article scraping, and AI generation
2. **Streamlit Frontend**: Provides a user-friendly interface for interacting with the application

## Project Structure

```
project_root/
├── main.py                # FastAPI backend
├── app.py                 # Streamlit frontend
├── requirements.txt       # Project dependencies
└── README.md              # Documentation
```

## Setup and Installation

1. Clone the repository
2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Running the Application

You need to run both the FastAPI backend and Streamlit frontend:

1. Start the FastAPI backend:
   ```
   uvicorn main:app --reload
   ```
   This will run the API at http://localhost:8000

2. In a separate terminal, start the Streamlit frontend:
   ```
   streamlit run app.py
   ```
   This will run the Streamlit app at http://localhost:8501

## Features

- Scrape articles from URLs using BeautifulSoup
- Generate LinkedIn posts using Google's Gemini AI
- Choose from multiple perspective options
- Receive confidence scores on alignment with "AI as enabler" philosophy
- User-friendly interface

## API Endpoints

- `GET /`: Root endpoint that returns a welcome message
- `POST /generate-post`: Generates a LinkedIn post based on article content

## Security Note

The API key for Google Gemini AI is hardcoded in the example. In a production environment, it's recommended to use environment variables or a secure key management system.

## License

[MIT License](LICENSE)