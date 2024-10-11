from pandas import DataFrame, Series


class PriorityBased:
    def __init__(self, data: DataFrame):
        self.movies = data
        self.filtered_movies = DataFrame()
        self.minimum_votes = 0
        self.all_votes_average = 0

    def load_data(self):
        self.minimum_votes = self.movies["vote_count"].quantile(0.9)
        self.all_votes_average = self.movies["vote_average"].mean()
        self.filtered_movies = self.movies.copy().loc[
            self.movies["vote_count"] >= self.minimum_votes
        ]

    def calculate_weighted_ratings(self):
        def weighted_rating(
            row: Series, min_votes: float, votes_average: float
        ) -> float:
            vote_average = row["vote_average"]
            vote_count = row["vote_count"]
            weighted = ((vote_count / (vote_count + min_votes)) * vote_average) + (
                min_votes / (vote_count + min_votes) * votes_average
            )
            return round(weighted, 3)

        self.filtered_movies["weighted_rating"] = self.filtered_movies.apply(
            weighted_rating, axis=1, args=(self.minimum_votes, self.all_votes_average)
        )
        self.filtered_movies.sort_values(
            by="weighted_rating", ascending=False, inplace=True
        )

    def get_movies_data(self) -> list:
        self.load_data()
        self.calculate_weighted_ratings()
        return self.filtered_movies.to_dict(orient="records")
