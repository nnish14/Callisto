# api.py

from fastapi import FastAPI
from stt_module import transcribe_audio, transcribe_live
from llm_module import query_llm
from tts_module import text_to_speech
from context_manager import log_conversation

app = FastAPI()
API_KEY = "3y1YEqg92DKEak8mlW8S40ylRhzTNiZm"  # Replace with your API key

@app.post("/voice-query/")
async def voice_query(audio_file: str = "../data/audio_samples/test1.wav"):
    # Step 1: Transcribe audio to text
    text = transcribe_audio(audio_file)
    print(f"User said: {text}")
    
    # Step 2: Send text to Mistral and get response
    response = query_llm(text, API_KEY)
    print(f"Callisto says: {response}")
    
    # Debug: Check if response is empty
    if not response:
        print("[DEBUG] No response from LLM, skipping TTS.")
    else:
        # Step 3: Convert response to speech
        text_to_speech(response)
    
    # Step 4: Log the conversation
    print("[DEBUG] About to log conversation...")
    log_conversation(text, response)
    print("[DEBUG] Conversation logged successfully!")
    
    return {"user_input": text, "response": response}

@app.post("/live-voice-query/")
async def live_voice_query():
    # Step 1: Transcribe live audio to text
    text = transcribe_live()
    if not text:
        return {"user_input": "", "response": "No speech detected."}
    print(f"User said: {text}")
    
    # Step 2: Send text to Mistral and get response
    response = query_llm(text, API_KEY)
    print(f"Callisto says: {response}")
    
    # Debug: Check if response is empty
    if not response:
        print("[DEBUG] No response from LLM, skipping TTS.")
    else:
        # Step 3: Convert response to speech
        text_to_speech(response)
    
    # Step 4: Log the conversation
    print("[DEBUG] About to log conversation...")
    log_conversation(text, response)
    print("[DEBUG] Conversation logged successfully!")
    
    return {"user_input": text, "response": response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)