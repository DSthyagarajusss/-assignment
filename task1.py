import os
import subprocess
from pydub import AudioSegment
import requests
from elevenlabs import ElevenLabs, VoiceSettings

def download_youtube_video(url):
    try:
        subprocess.run(['yt-dlp', '-x', '--audio-format', 'mp3', url], check=True)
    except Exception as e:
        print(f"Error downloading video: {e}")

def extract_audio(video_file):
    audio = AudioSegment.from_file(video_file)
    audio_file = "audio.mp3"
    audio.export(audio_file, format="mp3")
    return audio_file

def convert_audio_to_text(audio_file, deepgram_api_key):
    url = "https://api.deepgram.com/v1/listen"
    headers = {
        'Authorization': f'Token {deepgram_api_key}',
        'Content-Type': 'audio/mpeg'
    }
    
    with open(audio_file, 'rb') as f:
        response = requests.post(url, headers=headers, data=f)
        
    if response.status_code == 200:
        return response.json()["channel"]["alternatives"][0]["transcript"]
    else:
        raise Exception(f"Deepgram API error: {response.content}")

def generate_audio_from_text(text, eleven_labs_api_key):
    client = ElevenLabs(api_key=eleven_labs_api_key)
    audio = client.text_to_speech.convert(
        voice_id="pMsXgVXv3BLzUgSXRplE",
        optimize_streaming_latency="0",
        output_format="mp3_22050_32",
        text=text,
        voice_settings=VoiceSettings(
            stability=0.1,
            similarity_boost=0.3,
            style=0.2,
        ),
    )
    with open("output_audio.mp3", "wb") as audio_file:
        audio_file.write(audio)
    print("Audio generated successfully!")

def main(youtube_url, deepgram_api_key, eleven_labs_api_key):
    download_youtube_video(youtube_url)
   
    video_file = max([f for f in os.listdir() if f.endswith('.mp4')], key=os.path.getmtime)
    audio_file = extract_audio(video_file)
    text = convert_audio_to_text(audio_file, deepgram_api_key)
    print("Transcribed Text:", text)
    
    generate_audio_from_text(text, eleven_labs_api_key)

youtube_url = "https://youtu.be/1vOdWyba8nU?si=J_f5CXkpL0yd7o1z"
deepgram_api_key = "YOUR_DEEPGRAM_API_KEY"
eleven_labs_api_key = "YOUR_ELEVEN_LABS_API_KEY"

main(youtube_url, deepgram_api_key, eleven_labs_api_key)
