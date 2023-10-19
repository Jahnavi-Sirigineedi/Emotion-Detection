from flask import Flask, request, render_template
import os
import torchaudio
import requests
from pydub import AudioSegment
AudioSegment.converter = "ffmpeg-6.0"

from datasets import load_dataset
from pydub import AudioSegment
from pydub.playback import play

app = Flask(__name__)

# Define the location where user-uploaded audio files will be stored
UPLOAD_FOLDER = "Sound Recordings"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Function to download and process a dataset
def download_and_process_dataset(dataset_name, output_folder):
    dataset = load_dataset(dataset_name)
    for split in dataset.keys():
        split_data = dataset[split]
        for example in split_data:
            audio_url = example["path"]
            audio_path = os.path.join(output_folder, os.path.basename(audio_url))
            response = requests.get(audio_url)
            with open(audio_path, "wb") as audio_file:
                audio_file.write(response.content)

# Function to play an audio file
def play_audio(audio_path):
    sound = AudioSegment.from_mp3(audio_path)
    play(sound)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        uploaded_file = request.files["audio_file"]
        if uploaded_file:
            # Save the uploaded file
            file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
            uploaded_file.save(file_path)

            # Process the dataset (for example, CommonVoice)
            download_and_process_dataset("common_voice", "common_voice_data")

            # Example usage: Play a random audio file from the CommonVoice dataset
            random_audio_path = "common_voice_data/train/wav/Spanish-1857.wav"
            play_audio(random_audio_path)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
