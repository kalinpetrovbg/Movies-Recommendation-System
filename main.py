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
async def load_movies(request: Request):
    movies_data = movies.get_movies_data()
    return templates.TemplateResponse(
        "movies_table.html", {"request": request, "movies": movies_data}
    )

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8828)
