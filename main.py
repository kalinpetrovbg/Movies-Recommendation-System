from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse

from collaborative_based import CollaborativeBased
from data.scripts.movies_data import MovieData
from popularity_based import PriorityBased
from content_based import ContentBased
import uvicorn
from models.models import Movie, CollaborativeModel, ContentBasedModel

movies_csv = MovieData("data/movies.csv")
ratings_csv = MovieData("data/ratings.csv")
credits_csv = MovieData("data/credits.csv")

priority_data = PriorityBased(movies_csv.data)
content_data = ContentBased(movies_csv.data)
collaborative_data = CollaborativeBased(movies_csv.data)


templates = Jinja2Templates(directory="templates")
app = FastAPI()


@app.get("/", response_class=HTMLResponse, tags=["view"], include_in_schema=False)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.get(
    "/popularity", response_class=HTMLResponse, tags=["view"], include_in_schema=False
)
async def popularity(request: Request):
    movies_data = priority_data.get_movies_data()
    return templates.TemplateResponse(
        "popularity.html", {"request": request, "movies": movies_data}
    )


@app.get("/api/popularity", response_model=list[Movie], tags=["api"])
async def popularity_api():
    return priority_data.get_movies_data()



@app.get("/content/{movie_name}", tags=["view"], include_in_schema=False)
async def content(request: Request, movie_name: str):
    try:
        movies_data = content_data.get_movies_data(movie_name, number_of_movies=10)
    except IndexError:
        raise HTTPException(status_code=404, detail=f"Movie '{movie_name}' not found.")
    return templates.TemplateResponse(
        "content.html", {"request": request, "movies": movies_data}
    )




@app.get(
    "/api/content/{movie_name}",
    response_model=list[ContentBasedModel],
    tags=["api"],
)
async def content_api(movie_name: str):
    try:
        con_movies = content_data.get_movies_api_data(
            movie_name, number_of_movies=10
        )
    except IndexError:
        raise HTTPException(status_code=404, detail=f"Movie '{movie_name}' not found.")
    return [ContentBasedModel(**movie) for movie in con_movies]


@app.get("/collaborative", tags=["view"], include_in_schema=False)
async def collaborative(request: Request):
    return []


@app.get(
    "/api/collaborative", tags=["api"],
)
async def collaborative_api(movie_name: str):
    return []


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8828)
