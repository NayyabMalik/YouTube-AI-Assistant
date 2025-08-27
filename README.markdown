# YouTube AI Assistant

A Flask-based web application that allows users to input a YouTube video URL, transcribe its audio using the free Google Speech Recognition API, and ask questions about the video content using a chatbot powered by LangChain, FAISS, and OpenRouter's Mistral AI model. The tool is designed to be lightweight, free, and professional, suitable for extracting insights from YouTube videos.

## Features
- **Video Transcription**: Downloads audio from a YouTube video using `yt-dlp` and transcribes it in 30-second chunks using `SpeechRecognition` with Google’s free speech-to-text API.
- **Question Answering**: Processes the transcript with LangChain and FAISS for semantic search, allowing users to ask relevant questions (e.g., "Is the topic about peace?").
- **User-Friendly Interface**: A clean web interface with HTML, CSS, and JavaScript for entering URLs and questions, featuring loading animations and error handling.
- **Lightweight**: Uses free APIs and minimal local resources, ideal for web deployment.

## Prerequisites
- **Python**: 3.8 or higher
- **ffmpeg**: Required for audio extraction and conversion
- **Operating System**: Tested on Windows; compatible with Linux/macOS
- **OpenRouter Account**: For the Mistral AI model API key

## Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/NayyabMalik/YouTube-AI-Assistant
   cd youtube-ai-assistant
   ```

2. **Set Up Virtual Environment**:
   ```bash
   python -m venv myenv
   myenv\Scripts\activate  # Windows
   # source myenv/bin/activate  # Linux/macOS
   ```

3. **Install Dependencies**:
   ```bash
   pip install flask yt-dlp SpeechRecognition pydub langchain langchain-community langchain-huggingface langchain-openai python-dotenv
   ```

4. **Install `ffmpeg`**:
   - Download from [ffmpeg.org](https://ffmpeg.org/download.html) (Windows build).
   - Add `ffmpeg.exe` to `C:\Users\<YourUsername>\Documents\youtube Chatbot` or system PATH.
   - Verify: `ffmpeg -version`.

5. **Set Up Environment Variables**:
   - Create a `.env` file in the project root (`C:\Users\<YourUsername>\Documents\youtube Chatbot`):
     ```
     OPENROUTER_API_KEY=your-openrouter-api-key
     ```
   - Obtain an API key from [OpenRouter](https://openrouter.ai).

## Project Structure
```
youtube-ai-assistant/
├── app.py                  # Flask application
├── templates/
│   ├── index.html         # Main webpage
├── static/
│   ├── css/
│   │   ├── style.css      # Stylesheet
│   ├── js/
│   │   ├── script.js      # Frontend logic
├── .env                   # Environment variables
├── cleaned_transcript.txt # Generated transcript
├── faiss_index/          # FAISS vector store
├── audio.mp3             # Temporary audio file
├── audio.wav             # Temporary audio file
```

## Usage
1. **Run the Application**:
   ```bash
   python app.py
   ```
   - The app runs in debug mode by default (`http://127.0.0.1:5000`).

2. **Process a Video**:
   - Open `http://127.0.0.1:5000` in your browser.
   - Enter a YouTube URL (e.g., `https://youtu.be/TLKxdTmk-zc`).
   - Click "Process Video" to transcribe the audio and create a FAISS index (takes ~30-60 seconds for a 2-3 minute video).

3. **Ask Questions**:
   - Enter a question (e.g., "Is the topic about peace?").
   - Click "Ask Question" to get an answer based on the video’s transcript.

## Example
- **Video URL**: `https://youtu.be/TLKxdTmk-zc` (Mindfulness Meditation)
- **Question**: "Is the topic about peace?"
- **Expected Answer**: "Yes, the topic relates to peace through mindfulness meditation."


## Deployment
For production:
- Disable `debug=True` in `app.py` (`app.run()`).
- Use a WSGI server like Gunicorn:
  ```bash
  pip install gunicorn
  gunicorn -w 4 app:app
  ```
- Enable HTTPS with a reverse proxy (e.g., Nginx).
- Cache FAISS indexes for frequently accessed videos to reduce processing time.

## Notes
- **Free API**: Uses `SpeechRecognition` with Google’s free speech-to-text API (no key required), but rate limits may apply.
- **Video Content**: The app is tested with mindfulness videos (e.g., `https://youtu.be/TLKxdTmk-zc`). Ensure videos have clear audio for accurate transcription.
- **Scalability**: Pre-process transcripts offline and cache FAISS indexes for better performance.

## Contributing
Contributions are welcome! Submit issues or pull requests to improve functionality or fix bugs.

## License
MIT License © 2023

## Contact
For support, contact nayyabm16@gmail.com or open an issue on the repository.
