my_posts = [{"title": "title of post 1", "content": "content of post 1", "published": True, "rating": 2, "id": 1}, {
    "title": "title of post 2", "content": "content of post 2", "published": True, "rating": 2, "id": 2}]


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p


def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i
