from collections import Counter
from app.utils.helpers import first
def select(rows, limit):
    chosen, creators, categories = [], Counter(), Counter()
    for row in sorted(rows, key=lambda r: r["score"], reverse=True):
        post = row["post"]; creator = str(first(post, ["creator_id", "creatorId", "seller_id", "sellerId", "user_id"], "")); cat = str(first(post, ["category_id", "categoryId", "category"], ""))
        penalty = .08 * creators[creator] + .05 * categories[cat]
        if row["score"] - penalty > 0 or not chosen:
            row["score"] = round(row["score"] - penalty, 6); chosen.append(row); creators[creator] += 1; categories[cat] += 1
        if len(chosen) >= limit: break
    return chosen
