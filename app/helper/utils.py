import hashlib

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str) -> str:
    # Step 1: Pre-hash (removes length limit safely)
    sha256 = hashlib.sha256(password.encode("utf-8")).hexdigest()

    # Step 2: Bcrypt the hash
    return pwd_context.hash(sha256)


def verify_password(plane_password: str, hashed_password: str) -> bool:
    sha256 = hashlib.sha256(plane_password.encode("utf-8")).hexdigest()
    return pwd_context.verify(sha256, hashed_password)
