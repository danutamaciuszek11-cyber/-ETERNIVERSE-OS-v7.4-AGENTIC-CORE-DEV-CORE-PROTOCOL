import requests
import os

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")

class OllamaBridge:
    @staticmethod
    def generate(prompt: str, agent_role: str) -> str:
        url = f"{OLLAMA_HOST}/api/generate"
        payload = {
            "model": "llama3", # Default or configurable
            "prompt": f"You are {agent_role}, an AI agent in the ETERNIVERSE OS. {prompt}",
            "stream": False
        }
        try:
            response = requests.post(url, json=payload, timeout=30)
            if response.status_code == 200:
                return response.json().get("response", "")
            return f"[ERROR] Ollama returned status {response.status_code}"
        except requests.exceptions.RequestException as e:
            return f"[ERROR] Failed to connect to Ollama at {OLLAMA_HOST}. Is it running? Details: {e}"
