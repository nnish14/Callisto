# stt_module.py

import whisper
import os
import speech_recognition as sr

# Add ffmpeg to PATH (if needed)
ffmpeg_path = r"C:\Users\LENOVO\ffmpeg\ffmpeg-2025-03-20-git-76f09ab647-full_build\bin"
os.environ["PATH"] = ffmpeg_path + os.pathsep + os.environ["PATH"]

# Load Whisper model
MODEL_SIZE = "medium"
print(f"[DEBUG] Loading Whisper model: {MODEL_SIZE}")
model = whisper.load_model(MODEL_SIZE)
print("[DEBUG] Model loaded successfully!")

def transcribe_audio(file_path: str) -> str:
    """
    Transcribes an audio file using OpenAI Whisper.
    :param file_path: Path to input WAV/MP3/FLAC/M4A file.
    :return: Transcribed text string.
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"[STT] Audio file '{file_path}' does not exist.")

    print(f"[STT] Transcribing: {file_path}")
    result = model.transcribe(file_path, language="en")
    text = result.get("text", "")
    print(f"[STT] Transcribed text: {text}")
    return text

def transcribe_live() -> str:
    """
    Transcribes live audio from the microphone using speech_recognition.
    :return: Transcribed text string.
    """
    recognizer = sr.Recognizer()
    
    # Use the default microphone as the audio source
    with sr.Microphone() as source:
        print("[STT] Adjusting for ambient noise... Please wait.")
        recognizer.adjust_for_ambient_noise(source, duration=2)
        
        print("[STT] Listening... Speak now!")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            print("[STT] Processing audio...")
            # Use Google Speech Recognition (requires internet)
            text = recognizer.recognize_google(audio)
            print(f"[STT] Transcribed text: {text}")
            return text
        except sr.WaitTimeoutError:
            print("[STT] No speech detected within timeout.")
            return ""
        except sr.UnknownValueError:
            print("[STT] Could not understand the audio.")
            return ""
        except sr.RequestError as e:
            print(f"[STT] Error with speech recognition service: {e}")
            return ""

if __name__ == "__main__":
    # Test live transcription
    print("[DEBUG] Starting live STT test...")
    transcribed_text = transcribe_live()
    print(f"Live STT result: {transcribed_text}")