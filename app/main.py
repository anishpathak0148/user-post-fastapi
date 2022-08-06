import time
from typing import Union

from fastapi import FastAPI, Request
from app.api.user import router as user_router
from app.api.post import router as post_router

app = FastAPI()

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["response_time"] = f"{process_time} sec"
    return response

app.include_router(user_router)
app.include_router(post_router)


@app.get("/")
def read_root():
    return {"Hello": "World"}
