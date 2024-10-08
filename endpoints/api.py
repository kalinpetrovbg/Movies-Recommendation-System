from fastapi import APIRouter, HTTPException, Path
from pydantic import PositiveInt

from dependencies import (
    collaborative_data,
    content_data,
    movie_id_to_title,
    priority_data,
)
from models.models import CollaborativeModel, Movie, MovieRecommendation

router = APIRouter()


@router.get(
    "/api/popularity",
    response_model=list[Movie],
    tags=["api"],
    summary="Get the most popular movies.",
    description=(
        "Returns a list of movies ranked by popularity. "
        "It is based on a weighted rating system."
    ),
    response_description="A list of movies sorted by popularity.",
)
async def popularity_api():
    return priority_data.get_movies_data()


@router.get(
    "/api/content/{movie_name}/{num_movies}",
    response_model=list[MovieRecommendation],
    tags=["api"],
    summary="Get content-based movie recommendations.",
    description="Returns a list of movies similar to the specified movie.",
    response_description="A list of recommended movies.",
)
async def content_api(
    movie_name: str = Path(
        ..., min_length=2, description="Movie name for recommendations"
    ),
    num_movies: int = Path(..., gt=0, description="Number of movies to recommend"),
):
    try:
        movies_data = content_data.get_movies_data(movie_name, num_movies)
    except IndexError:
        raise HTTPException(status_code=404, detail=f"Movie '{movie_name}' not found.")
    return movies_data


@router.get(
    "/api/collaborative/{user_id}/{num_movies}",
    response_model=CollaborativeModel,
    tags=["api"],
    summary="Get collaborative filtering movie recommendations.",
    description=(
        "Returns a list of personalized movie recommendations for a specific user "
        "based on collaborative filtering algorithm."
    ),
    response_description="A dict containing the user ID and a list of recommended movies.",
)
async def collaborative_api(
    user_id: int = Path(..., gt=0, description="User ID"),
    num_movies: int = Path(..., gt=0, description="Number of movies to recommend"),
):
    try:
        recommendation_ids = collaborative_data.get_recommendations(user_id, num_movies)
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
