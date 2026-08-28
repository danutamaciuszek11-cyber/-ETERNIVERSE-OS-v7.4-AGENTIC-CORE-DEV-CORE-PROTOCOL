from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from ollama_bridge import OllamaBridge, AGENT_PERSONAS
import uvicorn
import os

app = FastAPI(title="Bellas API - Agentic Core (Multi-Agent Update)", version="7.5")

class PromptRequest(BaseModel):
    agent_id: str
    prompt: str

@app.get("/api/health")
def health_check():
    return {
        "status": "OPERATIONAL", 
        "module": "Bellas API (Aegis Core)", 
        "active_agents": list(AGENT_PERSONAS.keys())
    }

@app.post("/api/agents/generate")
def generate_agent_response(req: PromptRequest):
    # Walidacja agenta w oparciu o słownik z ollama_bridge
    if req.agent_id not in AGENT_PERSONAS:
        raise HTTPException(
            status_code=400, 
            detail=f"Nieznany Agent. Dostępni agenci: {', '.join(AGENT_PERSONAS.keys())}"
        )
    
    print(f"[AEGIS] Aktywacja agenta branżowego: {req.agent_id}...")
    print(f"[AEGIS] Spalanie 1 SOV z portfela użytkownika...")
    
    response = OllamaBridge.generate(req.prompt, req.agent_id)
    return {
        "agent": req.agent_id,
        "response": response,
        "tokens_burned": 1,
        "currency": "SOV",
        "status": "SUCCESS"
    }

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    print(f"⚡ BELLAS API (MULTI-AGENT) STARTUJE NA PORCIE {port}...")
    uvicorn.run(app, host="0.0.0.0", port=port)
