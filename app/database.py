from __future__ import annotations
import logging
from pymongo import MongoClient
from app.config import settings

log = logging.getLogger(__name__)
class Database:
    def __init__(self): self.client = None; self.db = None
    def connect(self):
        if not settings.mongo_uri: raise RuntimeError("MONGODB_URI is not configured")
        self.client = MongoClient(settings.mongo_uri, serverSelectionTimeoutMS=5000)
        self.client.admin.command("ping")
        name = settings.mongo_db_name or self._detect_db()
        self.db = self.client[name]; log.info("Database connected; selected database %s", name); return self.db
    def _detect_db(self):
        wanted = {"posts", "postembeddings", "postengagements"}
        matches = [(len(wanted & set(self.client[n].list_collection_names())), n) for n in self.client.list_database_names()]
        score, name = max(matches, default=(0, ""))
        if not score: raise RuntimeError("Could not identify a database containing assignment collections")
        return name
    def get_db(self):
        # PyMongo Database objects cannot be used with ``or``/boolean checks.
        return self.db if self.db is not None else self.connect()

database = Database()
