import pandas as pd
from surprise import SVD, Dataset, Reader


class CollaborativeBased:
    def __init__(self, ratings_file, movies_file):
        self.ratings = pd.read_csv(ratings_file)
        self.movies = pd.read_csv(movies_file)

        # Check for missing movies and filter ratings
        if not self.movies.empty:
            rated_movie_ids = set(self.ratings['movieId'].unique())
            existing_movie_ids = set(self.movies['id'].unique())
            missing_movie_ids = rated_movie_ids - existing_movie_ids

            if missing_movie_ids:
                self.ratings = self.ratings[
                    ~self.ratings['movieId'].isin(missing_movie_ids)]

        reader = Reader(rating_scale=(1, 5))
        dataset = Dataset.load_from_df(
            self.ratings[["userId", "movieId", "rating"]], reader
        )
        self.trainset = dataset.build_full_trainset()

        # Train the SVD algorithm
        self.svd = SVD()
        self.svd.fit(self.trainset)

    def get_recommendations(self, user_id, top_n=6):
        if not self.trainset.knows_user(user_id):
            raise ValueError(
                f"User ID {user_id} does not exist in the dataset")

        rated_movies = self.ratings[self.ratings["userId"] == user_id][
            "movieId"].tolist()

        all_movies = self.ratings["movieId"].unique()
        unrated_movies = [movie for movie in all_movies if
                          movie not in rated_movies]

        # Predict ratings for all unrated movies
        predictions = [self.svd.predict(user_id, movie_id) for movie_id in
                       unrated_movies]
        predictions.sort(key=lambda x: x.est, reverse=True)

        # Get the top N recommendations
        recommended_movie_ids = [int(pred.iid) for pred in predictions[:top_n]]

        return recommended_movie_ids