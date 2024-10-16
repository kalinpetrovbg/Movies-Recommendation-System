import pandas as pd
from numpy.core.defchararray import title


class MovieData:
    def __init__(self, file_path):
        self.data = pd.read_csv(file_path)

    def get_single_movie(self, movie_id):
        movie = self.data[self.data['id'] == movie_id]
        if not movie.empty:
            movie_dict = dict()
            for index, row in movie.iterrows():
                return [row]
        return "Movie Not Found!"

    def get_title_by_id(self, movie_id):
        title_row = self.data[self.data["id"] == movie_id]
        if not title_row.empty:
            return title_row.iloc[0]["title"]
        return "Title Not Found!"
