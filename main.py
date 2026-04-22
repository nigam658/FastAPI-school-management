from fastapi import FastAPI
from router import router as player_router

app = FastAPI()

app.include_router(player_router)