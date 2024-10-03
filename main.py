from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse
from popularity_based import PriorityBased
import uvicorn
from models.models import Movie

movies = PriorityBased("data/movies.csv")
movies.load_data()
movies.calculate_weighted_ratings()

templates = Jinja2Templates(directory="templates")
app = FastAPI()


@app.get("/", response_class=HTMLResponse, tags=["view"], include_in_schema=False)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/popularity", response_class=HTMLResponse, tags=["view"])
async def popularity(request: Request):
    movies_data = movies.get_movies_data()
    return templates.TemplateResponse(
        "popularity.html", {"request": request, "movies": movies_data}
    )


@app.get("/api/popularity", response_model=list[Movie], tags=["api"])
async def popularity_api():
    return movies.get_movies_data()


@app.get("/collaborative", response_class=HTMLResponse, deprecated=True, tags=["view"])
async def collaborative(request: Request):
    pass


@app.get(
    "/api/collaborative", response_model=list[Movie], deprecated=True, tags=["api"]
)
async def collaborative_api():
    return []


@app.get("/content", response_class=HTMLResponse, deprecated=True, tags=["view"])
async def content(request: Request):
    pass


@app.get("/api/content", response_model=list[Movie], deprecated=True, tags=["api"])
async def content_api():
    return []


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8828)
