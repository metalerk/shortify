from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_shorten_url_with_shortcode():
    with patch("app.data.repository.UrlRepository.save") as mock_save:
        mock_url = MagicMock(shortcode="abn123", update_id="mocked-update-id")
        mock_save.return_value = mock_url

        payload = {"url": "https://www.example.com/", "shortcode": "abn123"}
        response = client.post("/shorten", json=payload)

        assert response.status_code == 201
        assert response.json() == {
            "shortcode": "abn123",
            "update_id": "mocked-update-id",
        }
        mock_save.assert_called_once()


def test_shorten_url_without_shortcode():
    with patch("app.data.repository.UrlRepository.save") as mock_save:
        mock_url = MagicMock(shortcode="random123", update_id="mocked-update-id")
        mock_save.return_value = mock_url

        payload = {"url": "https://www.example.com/"}
        response = client.post("/shorten", json=payload)

        assert response.status_code == 201
        data = response.json()
        assert "shortcode" in data
        assert "update_id" in data
        mock_save.assert_called_once()
