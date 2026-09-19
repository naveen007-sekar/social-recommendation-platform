from __future__ import annotations
from datetime import datetime, timezone
from typing import Any
import numpy as np

def json_value(value: Any) -> Any:
    if isinstance(value, datetime): return value.isoformat()
    if isinstance(value, dict): return {str(k): json_value(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)): return [json_value(x) for x in value]
    if hasattr(value, "__str__") and value.__class__.__name__ == "ObjectId": return str(value)
    return value

def first(doc: dict, names: list[str], default=None):
    for name in names:
        if doc.get(name) is not None: return doc[name]
    return default

def vector(value: Any) -> np.ndarray | None:
    try:
        a = np.asarray(value, dtype=float).reshape(-1)
        return a if a.size and np.all(np.isfinite(a)) and np.linalg.norm(a) > 0 else None
    except (TypeError, ValueError): return None

def cosine(a: np.ndarray | None, b: np.ndarray | None) -> float:
    if a is None or b is None or a.shape != b.shape: return 0.0
    d = np.linalg.norm(a) * np.linalg.norm(b)
    return float(np.clip(np.dot(a, b) / d, 0, 1)) if d else 0.0

def timestamp(value: Any) -> datetime | None:
    if isinstance(value, datetime): return value if value.tzinfo else value.replace(tzinfo=timezone.utc)
    return None
