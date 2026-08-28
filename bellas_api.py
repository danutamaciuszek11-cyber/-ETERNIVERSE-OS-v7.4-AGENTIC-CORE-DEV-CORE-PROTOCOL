from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from ollama_bridge import OllamaBridge
import uvicorn
import os

app = FastAPI(title="Bellas API - Agentic Core", version="7.4")

class PromptRequest(BaseModel):
    agent_id: str
    prompt: str

@app.get("/api/health")
def health_check():
    return {"status": "OPERATIONAL", "module": "Bellas API", "layer": "Aegis Core"}

@app.post("/api/agents/generate")
def generate_agent_response(req: PromptRequest):
    allowed_agents = ["CINEMA", "CURATOR", "SCRIBE", "SENTINEL"]
    if req.agent_id not in allowed_agents:
        raise HTTPException(status_code=400, detail="Invalid Agent ID. Must be one of Bellas.")
    
    # In future, burn SOV token here before calling LLM
    print(f"[AEGIS] Burning 1 SOV for {req.agent_id} execution...")
    
    response = OllamaBridge.generate(req.prompt, req.agent_id)
    return {
        "agent": req.agent_id,
        "response": response,
        "tokens_burned": 1,
        "currency": "SOV"
    }

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    print(f"⚡ BELLAS API BOOTING ON PORT {port}...")
    uvicorn.run(app, host="0.0.0.0", port=port)
