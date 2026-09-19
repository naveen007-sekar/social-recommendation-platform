"""Read-only schema report. Never prints the configured URI."""
from collections import Counter
from app.database import database
from app.utils.helpers import json_value
def main():
    db=database.get_db(); print(f"Database selected: {db.name}")
    for name in db.list_collection_names():
        docs=list(db[name].find().limit(3)); keys=sorted({k for d in docs for k in d})
        print(f"\n{name}: {db[name].count_documents({})} documents\n  keys: {keys}")
        if name == "postembeddings":
            for d in docs:
                for k in ("embedding","vector","embeddings","post_embedding"):
                    if isinstance(d.get(k),list): print(f"  {k} dimension: {len(d[k])}")
        if name == "postengagements": print("  actions:", Counter(str(d.get("action",d.get("type",""))) for d in db[name].find()).most_common())
        if docs: print("  example:", json_value({k: docs[0][k] for k in keys if k not in {"embedding","vector"}}))
if __name__ == "__main__": main()
