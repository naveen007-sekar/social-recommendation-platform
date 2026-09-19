from app.config import settings
def score(parts: dict[str, float]) -> float:
    return sum(settings.rank_weights[k] * max(0., min(1., parts.get(k, 0.))) for k in settings.rank_weights)
