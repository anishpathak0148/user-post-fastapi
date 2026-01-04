from app.crud import user_crud, post_crud
from app.schema.user import UserCreate
from app.schema.post import PostBase
from app import models


import uuid


def test_user_crud_operations(db_session):
    # create user with unique email
    unique = uuid.uuid4().hex
    created_email = f"alice+{unique}@example.com"
    payload = UserCreate(name="Alice", email=created_email, password="secret")
    user = user_crud.create_user(db_session, payload)
    assert user.id is not None
    assert user.email == created_email

    # get by email
    fetched = user_crud.get_user_by_email(db_session, created_email)
    assert fetched is not None
    assert fetched.email == created_email

    # get users list
    users = user_crud.get_users(db_session)
    assert any(u.email == created_email for u in users)

    # update user
    new_payload = UserCreate(name="Alice B", email="aliceb@example.com", password="newpass")
    updated = user_crud.update_user(db_session, user_id=user.id, user=new_payload)
    assert updated.email == "aliceb@example.com"


def test_post_crud_operations(db_session):
    # create a user for post ownership
    unique = uuid.uuid4().hex
    user = models.User(name="Poster", email=f"poster+{unique}@example.com", hashed_password="x")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    post_title = f"Test Post {unique}"
    post_payload = PostBase(title=post_title, description="desc")
    post = post_crud.create_user_post(db_session, post=post_payload, user_id=user.id)
    assert post.id is not None
    assert post.title == post_title
    assert post.likes_count == 0

    # like post
    liked = post_crud.like_post(db_session, post_id=post.id, user_id=user.id)
    assert liked.likes_count == 1
    assert str(user.id) in liked.likes

    # update post
    upd_payload = PostBase(title="Updated", description="new")
    updated = post_crud.update_post(db_session, post=upd_payload, id=post.id)
    assert updated.title == "Updated"

    # delete post
    msg = post_crud.delete_post(db_session, id=post.id)
    assert "deleted" in msg.lower()
