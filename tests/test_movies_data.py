from unittest.mock import patch

import pandas as pd
import pytest

from data.scripts.movies_data import MovieData


@pytest.fixture
def test_data():
    return pd.DataFrame({"id": [1, 2, 3], "title": ["Titanic", "WALL·E", "Gladiator"]})


@patch("pandas.read_csv")
def test_get_title_by_id_found(mock_read_csv, test_data):
    mock_read_csv.return_value = test_data
    md = MovieData("dummy_path.csv")
    title = md.get_title_by_id(1)
    assert title == "Titanic"


@patch("pandas.read_csv")
def test_get_title_by_id_not_found(mock_read_csv, test_data):
    mock_read_csv.return_value = test_data
    md = MovieData("dummy_path.csv")
    title = md.get_title_by_id(4)
    assert title == "Title Not Found"
