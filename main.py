import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse

from collaborative_based import CollaborativeBased
from content_based import ContentBased
from data.scripts.movies_data import MovieData
from models.models import CollaborativeModel, ContentBasedModel, Movie
from popularity_based import PriorityBased

movies_csv = MovieData("data/movies.csv")
ratings_csv = MovieData("data/ratings.csv")
credits_csv = MovieData("data/credits.csv")

priority_data = PriorityBased(movies_csv.data)
content_data = ContentBased(movies_csv.data)
collaborative_data = CollaborativeBased(movies_csv.data)


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


@app.get("/content/{movie_name}", include_in_schema=False)
async def content(request: Request, movie_name: str):
    try:
        movies_data = content_data.get_movies_data(movie_name, number_of_movies=10)
    except IndexError:
        raise HTTPException(status_code=404, detail=f"Movie '{movie_name}' not found.")
    return templates.TemplateResponse(
        "content.html",
        {"request": request, "movies": movies_data, "movie_name": movie_name},
    )


@app.get("/collaborative", include_in_schema=False)
async def collaborative(request: Request):
    return []


@app.get("/api/popularity", response_model=list[Movie], tags=["api"])
async def popularity_api():
    return priority_data.get_movies_data()


@app.get(
    "/api/content/{movie_name}/{num_movies}",
    response_model=list[ContentBasedModel],
    tags=["api"],
)
async def content_api(movie_name: str, num_movies: int):
    try:
        movies_data = content_data.get_movies_data(movie_name, num_movies)
    except IndexError:
        raise HTTPException(status_code=404, detail=f"Movie '{movie_name}' not found.")
    return movies_data


@app.get(
    "/api/collaborative",
    tags=["api"],
)
async def collaborative_api():
    return []


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8828)
