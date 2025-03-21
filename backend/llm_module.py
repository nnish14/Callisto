# llm_module.py

import requests
from context_manager import get_conversation_history
from rag_module import RAGMemory

# Initialize RAG memory
rag = RAGMemory()

def query_llm(text: str, api_key: str) -> str:
    """
    Sends text to the Mistral API with conversation history and RAG context.
    :param text: The input text to process (e.g., transcribed speech).
    :param api_key: Your Mistral API key.
    :return: The response from the Mistral LLM.
    """
    # Get recent conversation history (last 3 turns)
    history = get_conversation_history(limit=3)
    messages = []
    
    # Add history to the messages
    for user_input, assistant_response in history:
        messages.append({"role": "user", "content": user_input})
        messages.append({"role": "assistant", "content": assistant_response})
    
    # Retrieve relevant context using RAG
    relevant_context = rag.retrieve_relevant_context(text, k=2)
    context_text = "\n".join([item["text"] for item in relevant_context])
    if context_text:
        messages.append({"role": "system", "content": f"Relevant past context:\n{context_text}"})
    
    # Add the current user input
    messages.append({"role": "user", "content": text})
    
    print(f"[LLM] Sending to Mistral with history and context: {messages}")
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "mistral-small",
        "messages": messages,
        "max_tokens": 200,
        "temperature": 0.7
    }
    print(f"[LLM] Request data: {data}")  # Debug: Print the full request
    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        result = response.json()
        answer = result["choices"][0]["message"]["content"]
        print(f"[LLM] Response: {answer}")
        
        # Add the user input and response to RAG memory
        rag.add_to_memory(text, {"timestamp": "2025-03-21", "type": "user"})
        rag.add_to_memory(answer, {"timestamp": "2025-03-21", "type": "assistant"})
        
        return answer
    except requests.exceptions.RequestException as e:
        print(f"[LLM] Error: {e}")
        # Print the response text for more details
        if hasattr(e, "response") and e.response is not None:
            print(f"[LLM] Error details: {e.response.text}")
        return ""

if __name__ == "__main__":
    api_key = "3y1YEqg92DKEak8mlW8S40ylRhzTNiZm"
    test_text = "Hello, how are you today?"
    response = query_llm(test_text, api_key)
    print(f"Test successful! Mistral says: {response}")