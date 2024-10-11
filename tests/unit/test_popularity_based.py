import pandas as pd

from app.algorithms.popularity_based import PriorityBased


def test_priority_based():
    mock_data = pd.DataFrame(
        {
            "id": [1, 2, 3, 4, 5],
            "title": ["Avatar", "Spectre", "Tangled", "Skyfall", "Brave"],
            "vote_count": [500, 150, 300, 800, 120],
            "vote_average": [8.5, 7.0, 6.5, 9.0, 5.5],
        }
    )

    priority = PriorityBased(mock_data)
    priority.load_data()
    priority.calculate_weighted_ratings()

    movies_data = priority.get_movies_data()

    assert len(movies_data) > 0
    assert all(
        movies_data[i]["weighted_rating"] >= movies_data[i + 1]["weighted_rating"]
        for i in range(len(movies_data) - 1)
    )

    assert "weighted_rating" in movies_data[0]
    assert "id" in movies_data[0]
    assert "title" in movies_data[0]

    top_movie = movies_data[0]
    assert top_movie["title"] == "Skyfall"
