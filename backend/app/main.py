from fastapi import FastAPI, HTTPException, Query, Header, Depends
from fastapi.middleware.cors import CORSMiddleware

from app.models.schemas import ChatRequest
from app.agents.orchestrator import Orchestrator
from app.security.guardrails import GuardrailError
import os, logging


app = FastAPI(
    title="ShopMuse AI",
    description="Multi-Agent Conversational Shopping Assistant"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173").split(","),
    allow_credentials=False,
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

    try:
        return orchestrator.run(request.session_id, request.message)
    except GuardrailError as e:
        raise HTTPException(status_code=422,detail=str(e))
    except Exception:
        logging.exception('Chat processing failed')
        raise HTTPException(status_code=503,detail='Shopping service temporarily unavailable')
# Read-only tool endpoints. Set SHOPMUSE_API_KEY to require a token.
def tool_auth(x_api_key: str | None = Header(default=None)):
    expected=os.getenv('SHOPMUSE_API_KEY')
    if expected and x_api_key != expected:raise HTTPException(401,'Unauthorized')

@app.get('/api/products',dependencies=[Depends(tool_auth)])
def products(category:str|None=None,max_price:float|None=Query(default=None,ge=0),limit:int=Query(default=30,ge=1,le=100)):
    return {'products':orchestrator.retrieval.tools.product_search(category=category,max_price=max_price,limit=limit)}

@app.get('/api/products/{product_id}',dependencies=[Depends(tool_auth)])
def product_details(product_id:str):
    product=orchestrator.retrieval.tools.product_details(product_id)
    if not product:raise HTTPException(404,'Product not found')
    return product

@app.get('/api/products/{product_id}/availability',dependencies=[Depends(tool_auth)])
def availability(product_id:str):
    return orchestrator.retrieval.tools.availability_price(product_id)

@app.get('/api/semantic-search',dependencies=[Depends(tool_auth)])
def semantic_search(q:str=Query(min_length=1,max_length=1000),category:str|None=None):
    return {'results':orchestrator.retrieval.tools.semantic_search(q,category)}

@app.get('/api/hybrid-search',dependencies=[Depends(tool_auth)])
def hybrid_search(q:str=Query(min_length=1,max_length=1000),category:str|None=None,max_price:float|None=Query(default=None,ge=0)):
    return orchestrator.retrieval.tools.hybrid_search(q,category,max_price)
