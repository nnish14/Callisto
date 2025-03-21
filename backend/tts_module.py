# tts_module.py

import pyttsx3

def text_to_speech(text: str) -> None:
    """
    Converts text to speech using pyttsx3.
    :param text: The text to speak.
    """
    print(f"[TTS] Speaking: {text}")
    try:
        engine = pyttsx3.init()
        engine.setProperty("rate", 150)  # Speed of speech (words per minute)
        engine.setProperty("volume", 0.9)  # Volume (0.0 to 1.0)
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"[TTS] Error: {e}")

if __name__ == "__main__":
    # Test the function
    test_text = "Hello, I am Callisto, your voice assistant!"
    text_to_speech(test_text)