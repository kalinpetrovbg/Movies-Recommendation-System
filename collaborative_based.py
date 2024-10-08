import pandas as pd
from surprise import SVD, Dataset, Reader


class CollaborativeBased:
    def __init__(self, ratings_file):
        self.ratings = pd.read_csv(ratings_file)
        reader = Reader(rating_scale=(1, 5))
        data = Dataset.load_from_df(
            self.ratings[["userId", "movieId", "rating"]], reader
        )
        self.trainset = data.build_full_trainset()

        # Train the SVD algorithm
        self.svd = SVD()
        self.svd.fit(self.trainset)

    def get_recommendations(self, user_id, top_n=6):
        if user_id not in self.trainset.all_users():
            return "User ID does not exist in the dataset"

        # Predict ratings for all movies that the user hasn't rated yet
        rated_movies = self.ratings[self.ratings["userId"] == user_id][
            "movieId"
        ].tolist()
        all_movies = self.ratings["movieId"].unique()
        unrated_movies = [movie for movie in all_movies if movie not in rated_movies]

        predictions = [
            self.svd.predict(user_id, movie_id) for movie_id in unrated_movies
        ]
        predictions.sort(key=lambda x: x.est, reverse=True)

        # Get the top N recommendations
        recommended_movie_ids = [pred.iid for pred in predictions[:top_n]]

        return recommended_movie_ids
