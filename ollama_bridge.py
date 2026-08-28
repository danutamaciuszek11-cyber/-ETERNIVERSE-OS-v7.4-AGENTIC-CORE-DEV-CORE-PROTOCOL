import requests
import os

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")

# Rejestr Agentów Branżowych z ich System Promptami (Osobowością)
AGENT_PERSONAS = {
    "NEXUS_LEX": "Jesteś NEXUS_LEX, elitarnym radcą prawnym i sztuczną inteligencją analityczną ETERNIVERSE OS. Twoim zadaniem jest analiza umów, identyfikacja kruczków prawnych i formułowanie zaleceń zgodnych z kodeksem. Odpowiadasz profesjonalnie, precyzyjnie i używasz terminologii prawniczej.",
    "NEXUS_BUILDER": "Jesteś NEXUS_BUILDER, cyber-architektem i inżynierem budowlanym. Analizujesz plany, dobierasz materiały i projektujesz struktury w świecie rzeczywistym i wirtualnym. Odpowiadasz konkretnie, skupiając się na fizyce, nośności materiałów i optymalizacji kosztów.",
    "KDP_SCRIBE": "Jesteś KDP_SCRIBE, pisarzem Quantum Manuscript Automaton. Jesteś mistrzem narracji, fabuły i budowania świata (worldbuilding). Twoim zadaniem jest kreowanie porywających opowieści, książek i dialogów dla wydawnictw KDP.",
    "CINEMA": "Jesteś CINEMA, modułem wizualizacji. Generujesz opisy scenerii, promptujesz generatory obrazów i dbasz o warstwę estetyczną Dominium Matrix.",
    "SENTINEL": "Jesteś SENTINEL, strażnikiem bezpieczeństwa ETERNIVERSE. Chronisz przed prompt-injection i analizujesz zagrożenia cyfrowe."
}

class OllamaBridge:
    @staticmethod
    def generate(prompt: str, agent_id: str) -> str:
        url = f"{OLLAMA_HOST}/api/generate"
        
        # Pobieranie osobowości lub użycie domyślnej
        system_prompt = AGENT_PERSONAS.get(
            agent_id, 
            f"Jesteś {agent_id}, bytem cyfrowym w systemie ETERNIVERSE OS."
        )
        
        full_prompt = f"SYSTEM: {system_prompt}\n\nUSER: {prompt}\n\nAGENT:"

        payload = {
            "model": "llama3", # Zmieniamy na mistral lub llama3 w zaleznosci od chmury
            "prompt": full_prompt,
            "stream": False,
            "options": {
                "temperature": 0.7
            }
        }
        
        try:
            response = requests.post(url, json=payload, timeout=30)
            if response.status_code == 200:
                return response.json().get("response", "")
            return f"[ERROR] Ollama zwróciła status {response.status_code}"
        except requests.exceptions.RequestException as e:
            return f"[ERROR] Brak fizycznego połączenia z modelem Ollama pod {OLLAMA_HOST}. Zbyt słaby sprzęt lub brak uruchomionego kontenera."
