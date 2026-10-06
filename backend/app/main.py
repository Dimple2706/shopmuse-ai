from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.models.schemas import ChatRequest
from app.agents.orchestrator import Orchestrator


app = FastAPI(
    title="ShopMuse AI",
    description="Multi-Agent Conversational Shopping Assistant"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


orchestrator = Orchestrator()


@app.get("/")
def home():

    return {
        "message": "Welcome to ShopMuse AI ♡"
    }


@app.post("/chat")
def chat(request: ChatRequest):

    result = orchestrator.run(
        request.session_id,
        request.message
    )

    return result