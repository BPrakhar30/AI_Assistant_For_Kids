import whisper
import pyaudio
import wave

class SpeechToText:
    def __init__(self, model_name="base"):
        self.model = whisper.load_model(model_name)

    def record_audio(self, filename, duration=5, rate=16000, channels=1):
        chunk = 1024  # Recording in chunks of 1024 samples
        format = pyaudio.paInt16  
        p = pyaudio.PyAudio()  # Creating an interface to PortAudio


        stream = p.open(format=format,
                        channels=channels,
                        rate=rate,
                        input=True,
                        frames_per_buffer=chunk)

        print("Recording...")
        frames = []

        # Recording for the specified duration
        for _ in range(0, int(rate / chunk * duration)):
            data = stream.read(chunk)
            frames.append(data)

        # Stoping and closing the stream
        stream.stop_stream()
        stream.close()
        p.terminate()

        # Saving the recorded data as a WAV file
        wf = wave.open(filename, 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(format))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))
        wf.close()
        print("Recording complete.")

    def transcribe_audio(self, filename):
        result = self.model.transcribe(filename)
        return result['text']

    def record_and_transcribe(self, filename="output.wav", duration=5):
        self.record_audio(filename, duration)
        return self.transcribe_audio(filename)

# Creating an instance of the SpeechToText class
speech_to_text = SpeechToText()

# Recording audio and transcribing it
transcription = speech_to_text.record_and_transcribe(duration=5)
print("Transcription:", transcription)
