from app.dependencies import get_db
from sqlalchemy.orm import Session


def test_get_db_generator():
    gen = get_db()
    db = next(gen)
    assert isinstance(db, Session)
    # close generator to run finally block
    try:
        gen.close()
    except RuntimeError:
        pass
