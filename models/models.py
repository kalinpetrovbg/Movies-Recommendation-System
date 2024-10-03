from pydantic import BaseModel

class Movie(BaseModel):
    title: str
    vote_count: int
    vote_average: float
    weighted_rating: float