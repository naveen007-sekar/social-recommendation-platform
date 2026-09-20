import logging
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from app.api.routes import router
logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
app=FastAPI(title="Social Commerce Post Recommender",version="1.0.0",docs_url="/docs",redoc_url="/redoc")
app.include_router(router)

static_dir = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/", include_in_schema=False)
def frontend():
    return FileResponse(static_dir / "index.html")
