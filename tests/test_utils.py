from app.helper.utils import get_hashed_password, verify_password


def test_get_hashed_and_verify():
    pw = "s3cret-pass"
    hashed = get_hashed_password(pw)
    assert isinstance(hashed, str) and len(hashed) > 0
    assert verify_password(pw, hashed) is True
    assert verify_password("wrong-pass", hashed) is False
