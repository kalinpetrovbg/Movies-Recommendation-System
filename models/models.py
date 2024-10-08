from pydantic import BaseModel
from typing import List

class Movie(BaseModel):
    id: int
    title: str
    vote_count: int
    vote_average: float
    weighted_rating: float


class MovieRecommendation(BaseModel):
    id: int
    title: str


class CollaborativeModel(BaseModel):
    user_id: int
    recommendations: List[MovieRecommendation]
