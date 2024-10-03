from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse
from popularity_based import PriorityBased
import uvicorn

movies = PriorityBased("data/movies.csv")
movies.load_data()
movies.calculate_weighted_ratings()

templates = Jinja2Templates(directory="templates")
app = FastAPI()

@app.get("/", response_class=HTMLResponse)
@app.get("/popularity", response_class=HTMLResponse)
async def popularity(request: Request):
    movies_data = movies.get_movies_data()
    return templates.TemplateResponse(
        "popularity.html", {"request": request, "movies": movies_data}
    )

@app.get("/collaborative", response_class=HTMLResponse, deprecated=True)
async def collaborative(request: Request):
    pass

@app.get("/content", response_class=HTMLResponse, deprecated=True)
async def content(request: Request):
    pass


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8828)
