from unittest.mock import patch

import pandas as pd

from app.algorithms.collaborative_based import CollaborativeBased


@patch("pandas.read_csv")
def test_get_recommendations_with_mock_data(mock_read_csv):
    mock_ratings = pd.DataFrame(
        {
            "userId": [1, 1, 2],
            "movieId": [10, 20, 30],
            "rating": [4.0, 5.0, 3.0],
        }
    )

    mock_movies = pd.DataFrame(
        {"id": [10, 20, 30], "title": ["Iron Man", "The Dark Knight", "Up"]}
    )

    mock_read_csv.side_effect = [mock_ratings, mock_movies]

    cb = CollaborativeBased("dummy_ratings.csv", "dummy_movies.csv")
    recommendations = cb.get_recommendations(user_id=1, top_n=2)

    assert len(recommendations) == 1
    assert recommendations[0]["title"] == "Up"
