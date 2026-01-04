def test_read_root(client):
    resp = client.get("/")
    assert resp.status_code == 200
    body = resp.json()
    # should return a Hello key with some string message
    assert "Hello" in body
    assert isinstance(body["Hello"], str)
