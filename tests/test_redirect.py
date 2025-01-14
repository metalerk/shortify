from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_redirect():
    with patch("app.data.repository.UrlRepository.find_by_shortcode") as mock_find:
        mock_url = MagicMock(url="https://www.example.com/")
        mock_find.return_value = mock_url

        response = client.get("/abn123", follow_redirects=False)

        assert response.status_code == 302
        assert response.headers["Location"] == "https://www.example.com/"
        mock_find.assert_called_once_with("abn123")
