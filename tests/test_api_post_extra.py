from app import models
from app.schema.user import User as PydUser


def test_get_nonexistent_post(client):
    resp = client.get("/posts/99999")
    assert resp.status_code == 404


def test_create_post_user_not_exist(client):
    # temporarily override current user to a non-existing user id
    from app.main import app as fastapi_app

    def fake_user():
        return PydUser(id=99999, name="no", email="no@example.com", is_active=True)

    fastapi_app.dependency_overrides[__import__("app.auth", fromlist=["get_current_active_user"]).get_current_active_user] = fake_user
    try:
        resp = client.post("/posts", json={"title": "no-user", "description": "x"})
        assert resp.status_code == 400
    finally:
        fastapi_app.dependency_overrides.pop(__import__("app.auth", fromlist=["get_current_active_user"]).get_current_active_user, None)


def test_update_post_unauthorized(db_session, client):
    # create owner and post
    owner = models.User(name="owner", email="owner@example.com", hashed_password="x")
    db_session.add(owner)
    db_session.commit()
    db_session.refresh(owner)

    post = models.Post(title="OwnerPost", description="d", user_id=owner.id)
    db_session.add(post)
    db_session.commit()
    db_session.refresh(post)

    # override current user to a different user
    from app.main import app as fastapi_app

    def other_user():
        return PydUser(id=owner.id + 1, name="other", email="other@example.com", is_active=True)

    fastapi_app.dependency_overrides[__import__("app.auth", fromlist=["get_current_active_user"]).get_current_active_user] = other_user
    try:
        resp = client.put(f"/posts/{post.id}", json={"title": "X", "description": "Y"})
        assert resp.status_code == 401
    finally:
        fastapi_app.dependency_overrides.pop(__import__("app.auth", fromlist=["get_current_active_user"]).get_current_active_user, None)


def test_like_post_already_liked(db_session, client):
    # create user and post, add like
    user = models.User(name="liker", email="liker@example.com", hashed_password="x")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    post = models.Post(title="LikedPost", description="d", user_id=user.id, likes=[str(user.id)], likes_count=1)
    db_session.add(post)
    db_session.commit()
    db_session.refresh(post)

    # override current_user to this user
    from app.main import app as fastapi_app

    def this_user():
        return PydUser(id=user.id, name=user.name, email=user.email, is_active=True)

    fastapi_app.dependency_overrides[__import__("app.auth", fromlist=["get_current_active_user"]).get_current_active_user] = this_user
    try:
        like_resp = client.post(f"/posts/posts/{post.id}/like")
        assert like_resp.status_code == 400
    finally:
        fastapi_app.dependency_overrides.pop(__import__("app.auth", fromlist=["get_current_active_user"]).get_current_active_user, None)
