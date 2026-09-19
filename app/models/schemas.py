from pydantic import BaseModel, Field
from typing import Any
class Recommendation(BaseModel):
    post_id: str; score: float; reason: list[str]; score_breakdown: dict[str, float]; post: dict[str, Any] = Field(default_factory=dict)
class RecommendationResponse(BaseModel):
    user_id: str; strategy: str; recommendations: list[Recommendation]
