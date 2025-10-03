from fastapi import FastAPI

from app.api.link import router


app = FastAPI()

app.include_router(router)
