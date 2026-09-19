def strategy(profile): return "hybrid_personalized" if profile is not None else "cold_start_trending_recent"
