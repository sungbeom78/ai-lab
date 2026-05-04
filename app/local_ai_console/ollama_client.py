import requests
import json

OLLAMA_BASE_URL = "http://localhost:11434"

def get_models():
    try:
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
        response.raise_for_status()
        data = response.json()
        return [model['name'] for model in data.get('models', [])]
    except Exception as e:
        return {"error": f"Failed to fetch models from Ollama: {str(e)}"}

def generate(model: str, prompt: str, temperature: float = 0.2):
    try:
        payload = {
            "model": model,
            "prompt": prompt,
            "temperature": temperature,
            "stream": False
        }
        response = requests.post(f"{OLLAMA_BASE_URL}/api/generate", json=payload, timeout=300)
        response.raise_for_status()
        return response.json().get("response", "")
    except Exception as e:
        return f"Error communicating with Ollama: {str(e)}"
