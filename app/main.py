from ast import While
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time


app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = 0


while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres',
                                password='1@Jean-Marie', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('Database connection was successfull!')
        break
    except Exception as error:
        print("Connection to database failed")
        print("Error: ", error)
        time.sleep(2)


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


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts ORDER BY id ASC""")
    posts = cursor.fetchall()
    # return {"data": my_posts}
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    # print(post)
    # print(post.dict())
    # print(post.published)
    # print(post.rating)
    # print(type(post))
    # post_dict = post.dict()
    # post_dict['id'] = randrange(0, 1000000)
    # my_posts.append(post_dict)
    # cursor.execute(
    #     f""" INSERT INTO posts (title, content, published, rating )
    #     VALUES ('{post.title}', '{post.content}', {post.published}, {post.rating}) """)

    cursor.execute(
        """ INSERT INTO posts (title, content, published, rating )
        VALUES (%s, %s, %s, %s) RETURNING * """, (post.title, post.content, post.published, post.rating))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data of the created post": new_post}


@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id)))
    post = cursor.fetchone()
    #post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id : {id} was not found")
    return {"post_detail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute(
        """DELETE FROM posts WHERE id = %s RETURNING * """, (str(id)))
    deleted_post = cursor.fetchone()
    conn.commit()
    # index = find_index_post(id)
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id : {id} does not exist")
    # my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts  SET title=%s, content=%s, published=%s, rating=%s WHERE id=%s RETURNING * """,
                   (post.title, post.content, post.published, post.rating, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    #index = find_index_post(id)
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id : {id} does not exist")
    # post_dict = post.dict()
    # post_dict["id"] = id
    #my_posts[index] = post_dict
    return {"Post Updated": updated_post}


"""
def create_posts(payLoad: dict = Body(...)):
    print(payLoad)
    return {"new_post": f"title :  {payLoad['title']};  content: {payLoad['content']}"}

"""


"""
post= my_posts[len(my_posts)-1]
this returns the lastest element appended to my_posts


we could have written:
response.status_code = 404
instead of 
response.status_code = status.HTTP_404_NOT_FOUND
Notice that status is imported from that packaage fastapi


def get_post(id: int, response: Response):
    post = find_post(id)
    if not post:        
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'message': f"post with id : {id} was not found"}
    return {"post_detail": post}
"""
# title str, content str, category, Bool
