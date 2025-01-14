from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_update_url():
    with patch("app.data.repository.UrlRepository.update_url") as mock_update:
        mock_url = MagicMock(shortcode="abn123")
        mock_update.return_value = mock_url

        payload = {"url": "https://www.new-example.com/"}
        response = client.post("/update/mocked-update-id", json=payload)

        assert response.status_code == 201
        assert response.json() == {"shortcode": "abn123"}
        mock_update.assert_called_once()
