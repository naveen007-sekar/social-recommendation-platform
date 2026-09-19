from __future__ import annotations
from collections import Counter
from typing import Any
from app.database import database
from app.utils.helpers import first, json_value

USER = ["user_id", "userId", "userid", "customer_id", "customerId"]
POST = ["post_id", "postId", "postid"]
CREATOR = ["creator_id", "creatorId", "seller_id", "sellerId", "user_id", "userId"]
PRODUCT = ["product_id", "productId"]

class DataService:
    def __init__(self, db=None):
        # PyMongo Database deliberately rejects truth-value testing.
        self.db = db if db is not None else database.get_db()
        self.names = set(self.db.list_collection_names())
    def docs(self, collection: str, query=None, limit=0):
        return list(self.db[collection].find(query or {}).limit(limit)) if collection in self.names else []
    def post_id(self, d): return str(first(d, POST + ["_id"], ""))
    def user_id(self, d): return str(first(d, USER, ""))
    def creator_id(self, d): return str(first(d, CREATOR, ""))
    def product_id(self, d): return str(first(d, PRODUCT, ""))
    def posts(self): return self.docs("posts", limit=0)
    def embeddings(self): return self.docs("postembeddings", limit=0)
    def post_embedding_map(self):
        out = {}
        for d in self.embeddings():
            pid = self.post_id(d)
            value = first(d, ["embedding", "vector", "embeddings", "post_embedding"])
            if pid and value is not None: out[pid] = value
        return out
    def by_user(self, collection, user_id): return [d for d in self.docs(collection) if self.user_id(d) == str(user_id)]
    def sample_users(self, n=10):
        users = Counter()
        for c in ("postengagements", "views", "carts", "orders"):
            for d in self.docs(c):
                if self.user_id(d): users[self.user_id(d)] += 1
        return [u for u, _ in users.most_common(n)]
    def followed_creators(self, user_id):
        ids = set()
        for d in self.by_user("follows", user_id):
            v = first(d, ["following_id", "followingId", "followed_id", "seller_id", "sellerId", "creator_id", "creatorId"])
            if v is not None: ids.add(str(v))
        return ids
    def product_categories(self):
        products = {self.product_id(p): p for p in self.docs("products")}
        return {pid: str(first(p, ["category_id", "categoryId", "product_category_id", "subcategory_id", "subCategoryId"], "")) for pid, p in products.items()}
    def public_post(self, post):
        keys = ["caption", "description", "title", "category", "category_id", "product_id", "createdAt", "created_at", "media"]
        return json_value({k: post[k] for k in keys if k in post})
