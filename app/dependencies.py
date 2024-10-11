from algorithms.collaborative_based import CollaborativeBased
from algorithms.content_based import ContentBased
from algorithms.popularity_based import PriorityBased
from fastapi.templating import Jinja2Templates

from app.database.movies_data import MovieData
from config import DATA_DIR, TEMPLATE_DIR

templates = Jinja2Templates(directory=str(TEMPLATE_DIR))

movies_csv = MovieData(DATA_DIR / "movies.csv")
priority_data = PriorityBased(movies_csv.data)
content_data = ContentBased(movies_csv.data)
collaborative_data = CollaborativeBased(
    DATA_DIR / "ratings.csv", DATA_DIR / "movies.csv"
)
movie_id_to_title = dict(zip(movies_csv.data["id"], movies_csv.data["title"]))
