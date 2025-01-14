from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_stats():
    with patch("app.data.repository.UrlRepository.find_by_shortcode") as mock_find:
        mock_url = MagicMock(
            shortcode=666,
            created=MagicMock(isoformat=lambda: "2023-01-01T12:00:00Z"),
            last_redirect=MagicMock(isoformat=lambda: "2023-01-02T12:00:00Z"),
            redirect_count=5,
        )
        mock_find.return_value = mock_url

        response = client.get("/abn123/stats")

        assert response.status_code == 200
        assert response.json() == {
            "shortcode": 666,
            "created": "2023-01-01T12:00:00Z",
            "lastRedirect": "2023-01-02T12:00:00Z",
            "redirectCount": 5,
        }
        mock_find.assert_called_once()
