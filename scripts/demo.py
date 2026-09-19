from app.services.data_service import DataService
from app.recommender.engine import RecommendationEngine
def main():
    service=DataService(); users=service.sample_users(1)
    if not users: print("No user behavior found."); return
    data=RecommendationEngine(service).recommend(users[0],10); print("User:",data["user_id"],"strategy:",data["strategy"])
    for r in data["recommendations"]: print(f"{r['post_id']} score={r['score']} | {', '.join(r['reason'])} | {r['score_breakdown']}")
if __name__ == "__main__": main()
