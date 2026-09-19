import logging
from fastapi import FastAPI
from app.api.routes import router
logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
app=FastAPI(title="Social Commerce Post Recommender",version="1.0.0")
app.include_router(router)
