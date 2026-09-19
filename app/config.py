from dataclasses import dataclass, field
import os
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Settings:
    mongo_uri: str | None = os.getenv("MONGODB_URI")
    mongo_db_name: str | None = os.getenv("MONGODB_DB_NAME") or None
    feedback_weights: dict[str, float] = field(default_factory=lambda: {"share": 5., "bookmark": 4., "save": 4., "comment": 3., "like": 2.})
    rank_weights: dict[str, float] = field(default_factory=lambda: {"content": .35, "behavioral": .20, "popularity": .15, "follow": .10, "commerce": .10, "recency": .10})
    recency_decay_days: float = 30.
    max_candidates: int = 1000

settings = Settings()
