from datetime import datetime, timezone
import math
from app.utils.helpers import first, timestamp
def popularity(metrics):
    raw=[]
    for m in metrics: raw.append(sum(math.log1p(float(first(m,[k],0) or 0)) for k in ["likes","comments","shares","saves","bookmarks"]))
    high=max(raw, default=0) or 1
    return {str(first(m,["post_id","postId","_id"],"")): raw[i]/high for i,m in enumerate(metrics)}
def recency(post, days):
    t=timestamp(first(post,["created_at","createdAt","published_at","publishedAt"]))
    return math.exp(-max(0,(datetime.now(timezone.utc)-t).days)/days) if t else 0.
