def candidates(posts, seen, minimum=30):
    unseen = [p for p in posts if str(p.get("_id")) not in seen]
    return unseen if len(unseen) >= minimum else posts
