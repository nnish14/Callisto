# context_manager.py

import os
from datetime import datetime

# Path to the session summary file
SESSION_FILE = "../data/session_summary.txt"

def log_conversation(user_input: str, assistant_response: str) -> None:
    """
    Logs the conversation to a file for context management.
    :param user_input: The user's input text.
    :param assistant_response: The assistant's response.
    """
    # Ensure the data directory exists
    os.makedirs(os.path.dirname(SESSION_FILE), exist_ok=True)
    
    # Get the current timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Log the conversation with a timestamp
    with open(SESSION_FILE, "a", encoding="utf-8") as f:
        f.write(f"--- Conversation at {timestamp} ---\n")
        f.write(f"User: {user_input}\n")
        f.write(f"Callisto: {assistant_response}\n\n")

def get_conversation_history(limit: int = 5) -> list:
    """
    Retrieves the last N conversation turns from the session file.
    :param limit: Number of recent conversations to retrieve.
    :return: List of (user_input, assistant_response) tuples.
    """
    if not os.path.exists(SESSION_FILE):
        return []
    
    conversations = []
    with open(SESSION_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    # Parse the file to extract conversations
    current_convo = {}
    for line in lines:
        line = line.strip()
        if line.startswith("--- Conversation at"):
            if current_convo.get("user") and current_convo.get("assistant"):
                conversations.append((current_convo["user"], current_convo["assistant"]))
            current_convo = {}
        elif line.startswith("User: "):
            current_convo["user"] = line[len("User: "):]
        elif line.startswith("Callisto: "):
            current_convo["assistant"] = line[len("Callisto: "):]
    
    # Add the last conversation if complete
    if current_convo.get("user") and current_convo.get("assistant"):
        conversations.append((current_convo["user"], current_convo["assistant"]))
    
    # Return the last 'limit' conversations
    return conversations[-limit:]

if __name__ == "__main__":
    # Test the functions
    log_conversation("Hello, how are you?", "Hi! I'm doing great, thanks for asking.")
    history = get_conversation_history()
    print("Recent conversations:")
    for user_input, assistant_response in history:
        print(f"User: {user_input}")
        print(f"Callisto: {assistant_response}\n")