import uuid


def test_user_api_create_and_list(client):
    # create a user via API with unique email
    unique = uuid.uuid4().hex
    payload = {
        "name": "API User",
        "email": f"apiuser+{unique}@example.com",
        "password": "pw",
    }
    resp = client.post("/users", json=payload)
    assert resp.status_code == 201
    body = resp.json()
    assert body["email"] == f"apiuser+{unique}@example.com"

    # list users
    resp = client.get("/users")
    assert resp.status_code == 200
    users = resp.json()
    assert any(u["email"] == f"apiuser+{unique}@example.com" for u in users)


def test_post_api_create_and_like(client):
    # create a post as the overridden current user with unique title
    unique = uuid.uuid4().hex
    payload = {"title": f"API Post {unique}", "description": "by API"}
    resp = client.post("/posts", json=payload)
    assert resp.status_code == 201
    post = resp.json()
    post_id = post["id"]

    # like the post (note route is /posts/posts/{id}/like based on router)
    like_resp = client.post(f"/posts/posts/{post_id}/like")
    assert like_resp.status_code == 200
    assert "liked successfully" in like_resp.json().get("message", "").lower()
