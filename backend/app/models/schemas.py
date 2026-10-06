from pydantic import BaseModel
from typing import Optional, List


class Constraint(BaseModel):
    name: str
    operator: str
    value: str
    importance: float = 1.0


class Intent(BaseModel):
    purchase_type: Optional[str] = None
    recipient: Optional[str] = None
    occasion: Optional[str] = None
    category: Optional[str] = None
    budget: Optional[float] = None
    preferences: List[str] = []
    confidence: float = 0.0


class ChatRequest(BaseModel):
    session_id: str
    message: str
    