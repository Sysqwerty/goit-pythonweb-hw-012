from unittest.mock import MagicMock, AsyncMock


def test_healthchecker_success(client, monkeypatch):
    # Mock get_db
    async def mock_get_db():
        mock_session = MagicMock()
        mock_session.execute = AsyncMock(
            return_value=MagicMock(scalar_one_or_none=AsyncMock(return_value=1))
        )
        yield mock_session

    monkeypatch.setattr("src.database.db.get_db", mock_get_db)

    # healthchecker
    response = client.get("/api/healthchecker")

    # Assertions
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to FastAPI!"}