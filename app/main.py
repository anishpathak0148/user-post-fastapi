import os
import time
from . import models
from typing import Union

import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, SessionLocal
from app.api.user import router as user_router
from app.api.post import router as post_router
from app.auth import router as auth_router

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

# Centralized logging configuration so module loggers obey the level
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["response_time"] = f"{process_time} sec"
    return response

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(post_router)


@app.get("/")
def read_root():
    output_stream = os.popen('echo "World! from $(hostname) and ip: $(hostname -I)"')
    msg = output_stream.read()
    return {"Hello": msg}
