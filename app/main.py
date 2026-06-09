from fastapi import FastAPI
from app.router.gmail_router import router as agent_router
from .database import engine
from .import models

models.Base.metadata.create_all(bind = engine)

app = FastAPI(
    title="Email Agent API"
)

app.include_router(agent_router)


@app.get("/")
def root():
    return {
        "message": "Email Agent API is running"
    }