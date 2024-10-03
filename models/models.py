from pydantic import BaseModel

class Movie(BaseModel):
    id: int
    title: str
    vote_count: int
    vote_average: float
    weighted_rating: float

class CollaborativeModel(BaseModel):
    id: int
    title: str