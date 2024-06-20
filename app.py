from flask import Flask, request, send_file, render_template
from werkzeug.utils import secure_filename
import os
from pydub import AudioSegment
from huffman import huffman_encode, huffman_decode

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads/'
COMPRESSED_FOLDER = 'static/compressed/'
ALLOWED_EXTENSIONS = {'mp3', 'wav', 'ogg', 'flac', 'aac'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(COMPRESSED_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['COMPRESSED_FOLDER'] = COMPRESSED_FOLDER

# Set explicit paths for ffmpeg and ffprobe
AudioSegment.converter = "C:/Users/Arifin/Downloads/ffmpeg-master-latest-win64-gpl/bin/ffmpeg.exe"
AudioSegment.ffprobe = "C:/Users/Arifin/Downloads/ffmpeg-master-latest-win64-gpl/bin/ffprobe.exe"

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compress', methods=['POST'])
def compress_audio():
    if 'file' not in request.files:
        return "No file part"
    
    file = request.files['file']
    
    if file.filename == '':
        return "No selected file"
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(upload_path)

        # Read the audio file using pydub
        audio = AudioSegment.from_file(upload_path)
        
        # Export to a format that can be played and compressed (e.g., m4a)
        compressed_filename = filename.rsplit('.', 1)[0] + "_compressed.m4a"
        compressed_path = os.path.join(app.config['COMPRESSED_FOLDER'], compressed_filename)
        
        # Normalize the audio if needed
        audio = audio.set_frame_rate(44100).set_channels(2).set_sample_width(2)
        audio.export(compressed_path, format="ipod", bitrate="128k")
        
        return send_file(compressed_path, as_attachment=True)
    
    return "Invalid file format"

if __name__ == "__main__":
    app.run(debug=True)
