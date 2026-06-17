# Smart Study Assistant

An AI-powered study assistant that transforms YouTube videos, uploaded videos, and audio files into structured learning resources.

## Features

* YouTube URL Processing
* Video File Upload Support
* Audio File Upload Support
* Speech-to-Text Transcription
* AI-Generated Notes
* Mind Map Generation
* Flashcard Generation
* PDF Export Functionality
* User-Friendly Streamlit Interface

## Tech Stack

### Frontend

* Streamlit

### Backend

* Python

### AI & NLP

* OpenAI Whisper
* Large Language Models (LLMs)

### Libraries

* yt-dlp
* FPDF
* Streamlit
* Whisper

## Project Workflow

1. User provides a YouTube URL or uploads a video/audio file.
2. Audio is extracted from the input source.
3. Whisper transcribes the audio into text.
4. The transcript is processed using AI models.
5. The system generates:

   * Transcript
   * Notes
   * Mind Map
   * Flashcards
6. Users can download the generated content as a PDF.

## Installation

### Clone the Repository

```bash
git clone https://github.com/Manu-25-ai/smart-study-assistant.git
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run the Application

```bash
streamlit run app.py
```

## Future Enhancements

* Multi-language support
* Advanced quiz generation
* User authentication
* Cloud deployment
* Learning progress tracking

## Author

Data Queen

## License

This project is developed for educational and internship purposes.
