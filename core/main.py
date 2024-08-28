from flask import Flask, jsonify, request, render_template, send_file, redirect, url_for, Blueprint, current_app
from flask_login import login_required, current_user
import os
from PyPDF2 import PdfReader
from pydub import AudioSegment
from gtts import gTTS

app = Flask(__name__)
main = Blueprint('main', __name__)

# Set the path to the FFmpeg executable
AudioSegment.converter = r"C:\\ffmpeg\\bin\\ffmpeg.exe"
AudioSegment.ffmpeg = r"C:\\ffmpeg\\bin\\ffmpeg.exe"
AudioSegment.ffprobe = r"C:\\ffmpeg\\bin\\ffmpeg.ffprobe"

def convert_pdf_to_audio(file_path, output_folder):
    try:
        # Convert PDF to text
        reader = PdfReader(file_path)
        text = ''
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text

        # Split text into chunks (approx. 100 characters each)
        chunk_size = 100
        chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

        audio_files = []
        for i, chunk in enumerate(chunks):
            tts = gTTS(chunk)
            audio_filename = f"part_{i + 1}.mp3"
            audio_path = os.path.join(output_folder, audio_filename)
            tts.save(audio_path)
            audio_files.append(audio_path)
            print(f"Saved audio file: {audio_path}")  # Log saved audio file path

        # Check if audio files were created
        if not audio_files:
            print("No audio files created.")
            return None

        # Combine audio files
        final_audio = combine_audio_files(audio_files)
        print(f"Final audio saved as: {final_audio}")  # Log the final audio file path

        # Cleanup temporary files
        for file in audio_files:
            os.remove(file)

        return os.path.basename(final_audio)
    except Exception as e:
        print(f"Error in conversion task: {e}")
        raise


@main.route('/')
def home():
    return render_template('home.html')

@main.route('/convert', methods=['GET', 'POST'])

def convert():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part', 400
        file = request.files['file']
        if file.filename == '':
            return 'No selected file', 400
        if file:
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)

            # Convert PDF to audio without async task
            final_audio_filename = convert_pdf_to_audio(file_path, current_app.config['OUTPUT_FOLDER'])

            # Redirect to the download page
            return redirect(url_for('main.download', filename=final_audio_filename))
    return render_template('convert.html')

def combine_audio_files(audio_files):
    combined = AudioSegment.empty()
    for audio_file in audio_files:
        print(f"Combining audio file: {audio_file}")  # Log each file being combined
        if not os.path.exists(audio_file):  # Check if file exists
            print(f"File does not exist: {audio_file}")
            raise FileNotFoundError(f"File not found: {audio_file}")  # Raise error if file is missing

        segment = AudioSegment.from_mp3(audio_file)
        combined += segment
    
    output_path = os.path.join(os.path.dirname(audio_files[0]), "final_audio.mp3")
    combined.export(output_path, format="mp3", codec="libmp3lame")
    return output_path


@main.route('/download/<filename>')

def download(filename):
    return render_template('download.html', filename=filename)

@main.route('/get-file/<filename>')

def get_file(filename):
    try:
        return send_file("C:\\Users\\HP\Downloads\\BookOwl\\os.path.join(os.getcwd(), 'static\\output')\\final_audio.mp3", as_attachment=True)
    except FileNotFoundError:
        return 'File not found', 404

@main.route('/payment')    
def payment():
    return render_template('payment.html')

if __name__ == "__main__":
    app.run(debug=True)
