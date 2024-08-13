import os
from dotenv import load_dotenv
from pathlib import Path
from pydub import AudioSegment
from pydub.playback import play
from openai import OpenAI

def generate_and_play_speech(text, output_dir="output", voice="Default"):
    # Loading environment variables from .env file
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")

    # Initializing the OpenAI client with the API key
    client = OpenAI(api_key=api_key)

    # Defining openai voices 
    voices = {
        "Dan": "onyx",
        "Default": "nova"
    }

    # Ensuring the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Dividing the script into manageable parts 
    parts = [text[i:i+4096] for i in range(0, len(text), 4096)]
    audio_segments = []

    # Generating TTS for each part
    for part in parts:
        response = client.audio.speech.create(
            model="tts-1",
            voice=voices.get(voice, "fable"),
            input=part,
            response_format='mp3'
        )
        part_audio_path = Path(output_dir) / "part_audio.mp3"
        with open(part_audio_path, 'wb') as audio_file:
            audio_file.write(response.content)
        part_audio = AudioSegment.from_file(part_audio_path)
        audio_segments.append(part_audio)

    # Combining the audio segments
    final_audio = sum(audio_segments)

    # Saving the final audio
    final_audio_path = Path(output_dir) / "final_audio.mp3"
    final_audio.export(final_audio_path, format="mp3")

    # Playing the final audio
    play(final_audio)

    return final_audio_path
