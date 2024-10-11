from typing import List

from pydantic import BaseModel


class BaseMovie(BaseModel):
    id: int
    title: str


class Movie(BaseMovie):
    weighted_rating: float
    vote_count: int
    vote_average: float
    release_date: str


class ContentModel(BaseMovie):
    similarity_score: float


class MovieRecommendation(BaseMovie):
    score: float


class CollaborativeModel(BaseModel):
    user_id: int
    recommendations: List[MovieRecommendation]
