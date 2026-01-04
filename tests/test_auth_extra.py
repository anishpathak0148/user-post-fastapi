import importlib
import os

from jose import jwt

from app import auth as auth_module


def test_authenticate_user_and_token(db_session):
    # create a user to authenticate
    from app.helper.utils import get_hashed_password
    from app import models

    u = models.User(name="auth", email="auth@example.com", hashed_password=get_hashed_password("pw"))
    db_session.add(u)
    db_session.commit()
    db_session.refresh(u)

    # authenticate_user should return a pydantic-like User object
    user = auth_module.authenticate_user(db_session, "auth@example.com", "pw")
    assert user is not False
    assert user.email == "auth@example.com"


def test_create_access_token_and_decode(monkeypatch):
    # set env vars and reload module so SECRET_KEY/ALGORITHM pick them up
    monkeypatch.setenv("SECRET_KEY", "test-secret-key-1234567890")
    monkeypatch.setenv("ALGORITHM", "HS256")
    importlib.reload(auth_module)

    token = auth_module.create_access_token({"sub": "me@example.com"})
    assert isinstance(token, str)
    decoded = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")])
    assert decoded.get("sub") == "me@example.com"
