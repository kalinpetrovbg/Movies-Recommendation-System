import pandas as pd


class MovieData:
    def __init__(self, file_path):
        self.data = pd.read_csv(file_path)

    def get_title_by_id(self, movie_id):
        title_row = self.data[self.data['id'] == movie_id]
        if not title_row.empty:
            return title_row.iloc[0]['title']
        return "Title Not Found"