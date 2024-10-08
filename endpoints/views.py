from fastapi import APIRouter, HTTPException, Request
from starlette.responses import HTMLResponse

from dependencies import (collaborative_data, content_data, movie_id_to_title,
                          priority_data, templates)

router = APIRouter()


@router.get("/", response_class=HTMLResponse, include_in_schema=False)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@router.get("/popularity", response_class=HTMLResponse, include_in_schema=False)
async def popularity(request: Request):
    movies_data = priority_data.get_movies_data()
    return templates.TemplateResponse(
        "popularity.html", {"request": request, "movies": movies_data}
    )


@router.get(
    "/content/{movie_name}/{num_movies}",
    response_class=HTMLResponse,
    include_in_schema=False,
)
async def content(request: Request, movie_name: str, num_movies: int):
    try:
        movies_data = content_data.get_movies_data(movie_name, num_movies)
    except IndexError:
        raise HTTPException(status_code=404, detail=f"Movie '{movie_name}' not found.")
    return templates.TemplateResponse(
        "content.html",
        {"request": request, "movies": movies_data, "movie_name": movie_name},
    )


@router.get(
    "/collaborative/{user_id}/{num_movies}",
    response_class=HTMLResponse,
    include_in_schema=False,
)
async def collaborative(request: Request, user_id: int, num_movies: int):
    try:
        recommendation_ids = collaborative_data.get_recommendations(user_id, num_movies)

        recommendations = [
            {
                "id": movie_id,
                "title": movie_id_to_title.get(movie_id, "Title Not Found"),
            }
            for movie_id in recommendation_ids
        ]

        return templates.TemplateResponse(
            "collaborative.html",
            {
                "request": request,
                "user_id": user_id,
                "recommendations": recommendations,
            },
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
