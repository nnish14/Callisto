# stt_module.py

import whisper
import os

# Load model once globally — pick your poison: tiny, base, small, medium, large
model = whisper.load_model("medium")

def transcribe_audio(file_path: str) -> str:
    """
    Transcribes an audio file using OpenAI Whisper.
    :param file_path: Path to input WAV/MP3/FLAC/M4A file.
    :return: Transcribed text string.
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"[STT] Audio file '{file_path}' does not exist.")

    print(f"[STT] Transcribing: {file_path}")
    result = model.transcribe(file_path,language="en")
    return result.get("text", "")
