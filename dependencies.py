from data.scripts.movies_data import MovieData
from popularity_based import PriorityBased
from content_based import ContentBased
from collaborative_based import CollaborativeBased
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

movies_csv = MovieData("data/movies.csv")
movies_csv.data["id"] = movies_csv.data["id"].astype(int)

priority_data = PriorityBased(movies_csv.data)
content_data = ContentBased(movies_csv.data)
collaborative_data = CollaborativeBased("data/ratings.csv")

movie_id_to_title = dict(
    zip(movies_csv.data["id"], movies_csv.data["title"])
)
