from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse

from collaborative_based import CollaborativeBased
from popularity_based import PriorityBased
import uvicorn
from models.models import Movie, CollaborativeModel

movies = PriorityBased("data/movies.csv")
movies.load_data()
movies.calculate_weighted_ratings()

collaboratives = CollaborativeBased("data/movies.csv")

templates = Jinja2Templates(directory="templates")
app = FastAPI()


@app.get("/", response_class=HTMLResponse, tags=["view"], include_in_schema=False)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.get(
    "/popularity", response_class=HTMLResponse, tags=["view"], include_in_schema=False
)
async def popularity(request: Request):
    movies_data = movies.get_movies_data()
    return templates.TemplateResponse(
        "popularity.html", {"request": request, "movies": movies_data}
    )


@app.get("/api/popularity", response_model=list[Movie], tags=["api"])
async def popularity_api():
    return movies.get_movies_data()


@app.get("/collaborative/{movie_name}", tags=["view"], include_in_schema=False)
async def collaborative(request: Request, movie_name: str):
    try:
        movies_data = collaboratives.get_movies_data(movie_name, number_of_movies=10)
    except IndexError:
        raise HTTPException(status_code=404, detail=f"Movie '{movie_name}' not found.")
    return templates.TemplateResponse(
        "collaborative.html", {"request": request, "movies": movies_data}
    )


@app.get(
    "/api/collaborative/{movie_name}",
    response_model=list[CollaborativeModel],
    tags=["api"],
)
async def collaborative_api(movie_name: str):
    try:
        coll_movies = collaboratives.get_movies_api_data(
            movie_name, number_of_movies=10
        )
    except IndexError:
        raise HTTPException(status_code=404, detail=f"Movie '{movie_name}' not found.")
    return [CollaborativeModel(**movie) for movie in coll_movies]


@app.get(
    "/content",
    response_class=HTMLResponse,
    deprecated=True,
    tags=["view"],
    include_in_schema=False,
)
async def content(request: Request):
    pass


@app.get("/api/content", response_model=list[Movie], deprecated=True, tags=["api"])
async def content_api():
    return []


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8828)
