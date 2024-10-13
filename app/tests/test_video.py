from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_upload_video():
    video_file = open("temp/file_example_MP4_480_1_5MG.mp4", "rb")
    response = client.post("/videos/upload", files={"file": video_file})
    assert response.status_code == 200
    assert response.json()["message"] == "Video upload initiated"


def test_search_video():
    response = client.get("/videos/search?name=test")
    assert response.status_code == 200


def test_blocked_video_download():
    response = client.get("/videos/download/2")
    assert response.status_code == 403
    assert response.json()["detail"] == "Video is blocked from downloading"
