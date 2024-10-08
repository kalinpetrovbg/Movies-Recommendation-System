from starlette import testclient

from app import app

client = testclient.TestClient(app)


def test_content_api():
    response = client.get("api/content/Avatar/5")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 5


def test_content_api_with_wrong_movie_name():
    response = client.get("api/content/AVTR/5")
    assert response.status_code == 404
    assert response.json() == {"detail": "Movie 'AVTR' not found."}


def test_content_api_with_zero_recommendations():
    response = client.get("/api/content/Avatar/0")
    assert response.status_code == 422


def test_popularity_api():
    response = client.get("api/popularity")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_collaborative_api():
    response = client.get("api/collaborative/2/5")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "user_id" in data
    assert "recommendations" in data
    assert data["user_id"] == 2


def test_collaborative_api_with_wrong_user_id():
    response = client.get("api/collaborative/-2/5")
    assert response.status_code == 422
    data = response.json()
    assert data["detail"][0]["msg"] == "Input should be greater than 0"


def test_collaborative_api_user_not_found():
    response = client.get("api/collaborative/99999999/5")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "User ID 99999999 does not exist in the dataset"
