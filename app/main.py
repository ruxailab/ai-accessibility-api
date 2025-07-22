from fastapi import FastAPI
from app.apis.routes import router

app = FastAPI(title="AI API")

app.include_router(router)
