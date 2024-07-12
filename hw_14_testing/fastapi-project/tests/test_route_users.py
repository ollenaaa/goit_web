import pytest
import io
import cloudinary
from unittest.mock import MagicMock, patch, AsyncMock
from fastapi_limiter import FastAPILimiter

from src.database.models import User
from src.schemas import UserModel
from src.services.auth import auth_service


def test_read_users_me(client, token):
    with patch.object(auth_service, 'cache') as r_mock:
        r_mock.get.return_value = None

        response = client.get(
            "/api/users/me",
            headers={"Authorization": f"Bearer {token}"})
        
        assert response.status_code == 200, response.text
        data = response.json()
        assert isinstance(data, dict)
        assert data["username"] == "deadpool"
        assert "id" in data


def test_update_avatar_user(client, token, user):
    with patch.object(auth_service, 'get_current_user') as mock_get_current_user, \
         patch.object(cloudinary.uploader, 'upload') as mock_upload:
        
        mock_get_current_user.get.return_value = None
        mock_upload.get.return_value = None
        
        files = {"file": ("filename.jpg", b"file_content", "image/jpeg")}
        
        response = client.patch(
            "/api/users/avatar",
            files=files,
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200, response.text
        data = response.json()
        assert isinstance(data, dict)
        assert data["username"] == "deadpool"
        assert "id" in data