from starlette import testclient

from app.main import app

client = testclient.TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200


def test_popularity():
    response = client.get("/popularity")
    assert response.status_code == 200


def test_content():
    response = client.get("/content/Avatar/5")
    assert response.status_code == 200


def test_non_existing_content():
    response = client.get("/content/WrongName/10")
    assert response.status_code == 404
    assert response.json() == {"detail": "Movie 'WrongName' not found."}


def test_collaborative():
    response = client.get("/collaborative/2/10")
    assert response.status_code == 200


def test_collaborative_with_wrong_user_id():
    response = client.get("/collaborative/-2/10")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "User ID -2 does not exist in the dataset"
    }
