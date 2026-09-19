from __future__ import annotations
from datetime import datetime, timezone
import numpy as np
from app.config import settings
from app.utils.helpers import first, vector, timestamp

def view_weight(doc):
    value = first(doc, ["view_percentage", "viewPercentage", "watch_percentage", "watchPercentage", "percentage"], 0)
    try: p = float(value)
    except (TypeError, ValueError): return 0.
    return 2.0 if p >= 90 else 1.3 if p >= 70 else .5 if p >= 40 else 0.

def build_profile(engagements, views, embeddings):
    weighted = []
    for d in list(engagements) + list(views):
        pid = str(first(d, ["post_id", "postId", "postid"], "")); emb = vector(embeddings.get(pid))
        action = str(first(d, ["action", "engagement_type", "type"], "")).lower()
        weight = settings.feedback_weights.get(action, view_weight(d))
        when = timestamp(first(d, ["created_at", "createdAt", "timestamp", "updatedAt"]))
        if when: weight *= float(np.exp(-max(0, (datetime.now(timezone.utc)-when).days) / 90))
        if emb is not None and weight > 0: weighted.append((emb, weight))
    if not weighted: return None
    dims = max(set(x.size for x, _ in weighted), key=lambda d: sum(v for x,v in weighted if x.size == d))
    weighted = [(x,w) for x,w in weighted if x.size == dims]
    return np.average(np.vstack([x for x,_ in weighted]), axis=0, weights=[w for _,w in weighted]) if weighted else None
