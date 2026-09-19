from __future__ import annotations
from collections import Counter
import logging
from app.config import settings
from app.services.data_service import DataService
from app.utils.helpers import cosine, first, vector
from .user_profile import build_profile
from .candidate_generator import candidates
from .feature_builder import popularity, recency
from .ranker import score
from .diversity import select
from .cold_start import strategy

log = logging.getLogger(__name__)
class RecommendationEngine:
    def __init__(self, service: DataService | None = None):
        self.data = service if service is not None else DataService()
    def recommend(self, user_id: str, limit=10):
        posts = self.data.posts()
        if not posts: return {"user_id": str(user_id), "strategy": "no_posts", "recommendations": []}
        embs = self.data.post_embedding_map(); engagements = self.data.by_user("postengagements", user_id); views = self.data.by_user("views", user_id)
        profile = build_profile(engagements, views, embs)
        seen = {str(first(x,["post_id","postId","postid"],"")) for x in engagements + views}
        follows = self.data.followed_creators(user_id)
        metrics = popularity(self.data.docs("postmetrics"))
        category_pref = self._category_preferences(user_id, engagements, views)
        rows=[]
        for post in candidates(posts, seen):
            pid=self.data.post_id(post); creator=self.data.creator_id(post); category=str(first(post,["category_id","categoryId","category","product_category_id"],""))
            content=cosine(profile, vector(embs.get(pid)))
            behavioral=min(1., category_pref["post"].get(pid,0.) + category_pref["category"].get(category,0.))
            commerce=category_pref["commerce"].get(category,0.)
            parts={"content":content,"behavioral":behavioral,"popularity":metrics.get(pid,0.),"follow":float(creator in follows),"commerce":commerce,"recency":recency(post,settings.recency_decay_days)}
            reasons=[]
            labels={"content":"Similar to posts you engaged with","behavioral":"Matches your engagement interests","popularity":"Popular with users","follow":"From a creator you follow","commerce":"Matches your shopping interests","recency":"Recently published"}
            for k, label in labels.items():
                if parts[k] >= (.15 if k in ("content","behavioral","commerce") else .35): reasons.append(label)
            if not reasons: reasons=["Trending and recent content"]
            rows.append({"post":post,"post_id":pid,"score":score(parts),"score_breakdown":{k:round(v,4) for k,v in parts.items()},"reason":reasons})
        result=[]
        for r in select(rows, max(1,min(int(limit),50))):
            result.append({"post_id":r["post_id"],"score":round(r["score"],4),"score_breakdown":r["score_breakdown"],"reason":r["reason"],"post":self.data.public_post(r["post"])})
        selected_strategy=strategy(profile); log.info("Generated %d recommendations using %s",len(result),selected_strategy)
        return {"user_id":str(user_id),"strategy":selected_strategy,"recommendations":result}
    def _category_preferences(self,user,engagements,views):
        post_lookup={self.data.post_id(p):p for p in self.data.posts()}; cats=Counter(); post_scores=Counter()
        for d, weight in [(d,1.) for d in engagements]+[(d,.4) for d in views]:
            pid=str(first(d,["post_id","postId","postid"],"")); post_scores[pid]+=weight
            if pid in post_lookup: cats[str(first(post_lookup[pid],["category_id","categoryId","category","product_category_id"],""))]+=weight
        commerce=Counter(); product_cats=self.data.product_categories()
        for c in ("carts","orders"):
            for d in self.data.by_user(c,user):
                pid=self.data.product_id(d)
                if pid in product_cats: commerce[product_cats[pid]]+=1
        norm=lambda x:{k:v/max(x.values()) for k,v in x.items()} if x else {}
        return {"post":norm(post_scores),"category":norm(cats),"commerce":norm(commerce)}
