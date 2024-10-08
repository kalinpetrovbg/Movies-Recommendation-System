import logging

import numpy as np
import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse

from collaborative_based import CollaborativeBased
from content_based import ContentBased
from data.scripts.movies_data import MovieData
from models.models import CollaborativeModel, MovieRecommendation, Movie
from popularity_based import PriorityBased

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

movies_csv = MovieData("data/movies.csv")
priority_data = PriorityBased(movies_csv.data)
content_data = ContentBased(movies_csv.data)
collaborative_data = CollaborativeBased("data/ratings.csv")


templates = Jinja2Templates(directory="templates")
app = FastAPI()


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/popularity", response_class=HTMLResponse, include_in_schema=False)
async def popularity(request: Request):
    movies_data = priority_data.get_movies_data()
    return templates.TemplateResponse(
        "popularity.html", {"request": request, "movies": movies_data}
    )


@app.get("/content/{movie_name}", response_class=HTMLResponse, include_in_schema=False)
async def content(request: Request, movie_name: str):
    try:
        movies_data = content_data.get_movies_data(movie_name, number_of_movies=10)
    except IndexError:
        raise HTTPException(status_code=404, detail=f"Movie '{movie_name}' not found.")
    return templates.TemplateResponse(
        "content.html",
        {"request": request, "movies": movies_data, "movie_name": movie_name},
    )


@app.get("/collaborative/{user_id}", response_class=HTMLResponse, include_in_schema=False)
async def collaborative(request: Request, user_id: int):
    try:
        recommendation_ids = collaborative_data.get_recommendations(user_id, 6)

        recommendations = [
            {"id": movie_id, "title": movies_csv.get_title_by_id(movie_id)}
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


@app.get("/api/popularity", response_model=list[Movie], tags=["api"])
async def popularity_api():
    return priority_data.get_movies_data()


@app.get(
    "/api/content/{movie_name}/{num_movies}",
    response_model=list[MovieRecommendation],
    tags=["api"],
)
async def content_api(movie_name: str, num_movies: int):
    try:
        movies_data = content_data.get_movies_data(movie_name, num_movies)
    except IndexError:
        raise HTTPException(status_code=404, detail=f"Movie '{movie_name}' not found.")
    return movies_data


@app.get("/api/collaborative/{user_id}", response_model=CollaborativeModel, tags=["api"])
async def collaborative_api(user_id: int):
    try:
        recommendation_ids = collaborative_data.get_recommendations(user_id, 6)
        recommendations = [
            {
                "id": movie_id,
                "title": movies_csv.get_title_by_id(movie_id)
            }
            for movie_id in recommendation_ids
        ]

        return {"user_id": user_id, "recommendations": recommendations}

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8828)
