from app.recommender.cold_start import strategy
from app.recommender.candidate_generator import candidates
def test_cold_start_and_seen_fallback():
    assert strategy(None) == "cold_start_trending_recent"
    assert len(candidates([{"_id":"a"}], {"a"}, minimum=30)) == 1
