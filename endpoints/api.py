from fastapi import APIRouter, HTTPException
from models.models import CollaborativeModel, Movie, MovieRecommendation

from dependencies import (
    priority_data,
    content_data,
    collaborative_data,
    movie_id_to_title,
)

router = APIRouter()


@router.get("/api/popularity", response_model=list[Movie], tags=["api"])
async def popularity_api():
    return priority_data.get_movies_data()


@router.get(
    "/api/content/{movie_name}/{num_movies}",
    response_model=list[MovieRecommendation],
    tags=["api"],
)
async def content_api(movie_name: str, num_movies: int):
    try:
        movies_data = content_data.get_movies_data(movie_name, num_movies)
    except IndexError:
        raise HTTPException(
            status_code=404, detail=f"Movie '{movie_name}' not found."
        )
    return movies_data


@router.get(
    "/api/collaborative/{user_id}", response_model=CollaborativeModel, tags=["api"]
)
async def collaborative_api(user_id: int):
    try:
        recommendation_ids = collaborative_data.get_recommendations(user_id, 6)
        recommendations = [
            {
                "id": movie_id,
                "title": movie_id_to_title.get(movie_id, "Title Not Found"),
            }
            for movie_id in recommendation_ids
        ]

        return {"user_id": user_id, "recommendations": recommendations}

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
