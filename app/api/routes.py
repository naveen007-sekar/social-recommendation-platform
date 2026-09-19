from fastapi import APIRouter, HTTPException, Query
from app.database import database
from app.services.data_service import DataService
from app.recommender.engine import RecommendationEngine

router=APIRouter()
@router.get("/health")
def health():
    try: database.get_db().command("ping"); return {"status":"healthy","database":"connected"}
    except Exception as exc: return {"status":"degraded","database":"unavailable","detail":str(exc)}
@router.get("/users/sample")
def sample_users():
    try: return {"user_ids":DataService().sample_users()}
    except Exception as exc: raise HTTPException(503, f"Database unavailable: {exc}")
@router.get("/recommend/{user_id}")
def recommend(user_id:str, limit:int=Query(10,ge=1,le=50)):
    try: return RecommendationEngine().recommend(user_id,limit)
    except Exception as exc: raise HTTPException(503, f"Recommendation unavailable: {exc}")
