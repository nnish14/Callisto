from stt_module import transcribe_audio

# Provide a short WAV/MP3 clip here (record yourself saying something)
audio_path = "test1.wav"

transcription = transcribe_audio(audio_path)
print(f"[TRANSCRIPTION RESULT]:\n{transcription}")
