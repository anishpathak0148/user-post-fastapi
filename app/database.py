import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")
SQLALCHEMY_DB_USER = os.getenv("POSTGRES_USER")
SQLALCHEMY_DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
SQLALCHEMY_DB = os.getenv("POSTGRES_DB")
SQLALCHEMY_DB_HOST = os.getenv("POSTGRES_SERVER")

SQLALCHEMY_DATABASE_URL = URL.create(
    "postgresql",
    username=SQLALCHEMY_DB_USER,
    password=SQLALCHEMY_DB_PASSWORD,  # plain (unescaped) text
    host=SQLALCHEMY_DB_HOST,
    port=5432,
    database=SQLALCHEMY_DB,
)

print(f"SQLALCHEMY_DATABASE_URL is: {SQLALCHEMY_DATABASE_URL}")

# Create SqlAlchemy engine
# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
# )
# Remove check_same_thread- it is an argument specific to sqlite.
engine = create_engine(SQLALCHEMY_DATABASE_URL)


# Create a SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a Base class
Base = declarative_base()
