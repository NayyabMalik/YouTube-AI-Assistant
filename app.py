from flask import Flask, request, render_template, jsonify
import os
from yt_dlp import YoutubeDL
import speech_recognition as sr
from pydub import AudioSegment
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from langchain.retrievers import MultiQueryRetriever
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

app = Flask(__name__)

# Load environment variables
load_dotenv()

# Initialize embeddings and LLM
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
llm = ChatOpenAI(
    model="mistralai/mixtral-8x7b-instruct",
    base_url="https://openrouter.ai/api/v1",
    temperature=0.0,
    max_tokens=512,
)

# Prompt template
prompt = PromptTemplate(
    template="""You are a helpful assistant. Answer the question based solely on the provided context. If the question cannot be answered from the context, respond with "I don't know."
Context: {context}
Question: {question}
Answer: """,
    input_variables=["context", "question"]
)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/process_video", methods=["POST"])
def process_video():
    try:
        video_url = request.form["video_url"]
        if not video_url.startswith("https://youtu.be/"):
            return jsonify({"error": "Invalid YouTube URL."}), 400

        # Step 1: Download audio
        ydl_opts = {
            'format': 'bestaudio',
            'outtmpl': 'audio.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        # Step 2: Convert MP3 to WAV (mono, 16kHz for Google)
        audio = AudioSegment.from_mp3("audio.mp3")
        audio = audio.set_channels(1).set_frame_rate(16000)
        audio.export("audio.wav", format="wav")

        # Step 3: Transcribe audio in chunks
        recognizer = sr.Recognizer()
        transcript_parts = []
        with sr.AudioFile("audio.wav") as source:
            while True:
                audio_data = recognizer.record(source, duration=30)
                if not audio_data.frame_data:
                    break
                try:
                    part = recognizer.recognize_google(audio_data, language="en-US")
                    transcript_parts.append(part)
                except sr.UnknownValueError:
                    continue
                except sr.RequestError as e:
                    return jsonify({"error": f"Google Speech API error: {e}"}), 500

        # Step 4: Merge and clean transcript
        cleaned_transcript = " ".join(transcript_parts).strip()
        if not cleaned_transcript:
            return jsonify({"error": "Transcription failed. Audio may be unintelligible."}), 500

        # Step 5: Save transcript
        with open("cleaned_transcript.txt", "w", encoding="utf-8") as file:
            file.write(cleaned_transcript)

        # Step 6: Create FAISS vector store
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
        docs = text_splitter.split_text(cleaned_transcript)
        if not docs:
            return jsonify({"error": "No valid text chunks for indexing."}), 500
        vector_store = FAISS.from_texts(docs, embeddings)
        vector_store.save_local("faiss_index")

        # Clean up audio files
        for file in ["audio.mp3", "audio.wav"]:
            if os.path.exists(file):
                os.remove(file)

        return jsonify({"message": "Video processed successfully. Ask a question!"})

    except Exception as e:
        return jsonify({"error": f"Error processing video: {str(e)}"}), 500

@app.route("/ask_question", methods=["POST"])
def ask_question():
    try:
        question = request.form["question"]
        if not os.path.exists("cleaned_transcript.txt"):
            return jsonify({"error": "No transcript available. Process a video first."}), 400

        # Load FAISS index
        vector_store = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
        retriever = MultiQueryRetriever.from_llm(
            retriever=vector_store.as_retriever(search_kwargs={"k": 2}),
            llm=llm,
        )

        # Query and answer
        result_ret = retriever.invoke(question)
        text_join = "\n\n".join([doc.page_content for doc in result_ret])
        parser = StrOutputParser()
        chain = prompt | llm | parser
        answer = chain.invoke({"question": question, "context": text_join})

        return jsonify({"answer": answer})

    except Exception as e:
        return jsonify({"error": f"Error answering question: {str(e)}"}), 500

if __name__ == "__main__":
    app.run()