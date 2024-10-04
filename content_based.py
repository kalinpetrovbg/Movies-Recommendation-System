from pandas import DataFrame, Series
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

tfidf = TfidfVectorizer(stop_words="english")


class ContentBased:
    def __init__(self, data: DataFrame):
        self.movies = data
        self.clean_empty_overview_data()
        self.tfidf_matrix = tfidf.fit_transform(self.movies["overview"])
        self.similarity_matrix = linear_kernel(self.tfidf_matrix, self.tfidf_matrix)

    def clean_empty_overview_data(self):
        self.movies["overview"] = self.movies["overview"].fillna("")
        return self.movies

    def get_similar_movies(self, title, number_of_movies):
        idx = self.movies.loc[self.movies["title"] == title].index[0]

        # Get similarity scores
        scores = list(enumerate(self.similarity_matrix[idx]))
        scores = sorted(scores, key=lambda x: x[1], reverse=True)

        movies_indices = [score[0] for score in scores[
                                                1:number_of_movies + 1]]

        similar_movies = [
            {
                "id": self.movies.iloc[index]["id"],
                "title": self.movies.iloc[index]["title"]
            }
            for index in movies_indices
        ]

        return similar_movies

    def get_movies_data(self, movie_name, number_of_movies):
        movies = self.get_similar_movies(movie_name, number_of_movies)
        return movies

