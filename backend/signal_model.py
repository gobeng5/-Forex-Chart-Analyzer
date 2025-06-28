from pydantic import BaseModel

class Signal(BaseModel):
    symbol: str
    direction: str
    entry: float
    sl: float
    tp: float
    confidence: int
