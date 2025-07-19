from pydantic import BaseModel
from typing import List, Optional

class RecommendationRequest(BaseModel):
    user_id: int
    limit: Optional[int] = 10

class EventResponse(BaseModel):
    id: int
    title: str
    description: str
    category_name: str
    similarity_score: Optional[float] = None

class RecommendationResponse(BaseModel):
    user_id: int
    recommended_events: List[EventResponse]
    message: str
