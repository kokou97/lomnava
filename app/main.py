from ast import While
from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models, schemas
from .database import engine, get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


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


@app.get("/posts", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts ORDER BY id ASC""")
    # posts = cursor.fetchall()
    # return {"data": my_posts}

    posts = db.query(models.Post).all()

    # posts = db.query(models.Post)
    # print(posts)
    # print in the console the sql query used to get posts
    return posts


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
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

    # cursor.execute(
    #     """ INSERT INTO posts (title, content, published, rating )
    #     VALUES (%s, %s, %s, %s) RETURNING * """, (post.title, post.content, post.published, post.rating))
    # new_post = cursor.fetchone()
    # conn.commit()
    # new_post = models.Post(
    #     title=post.title, content=post.content, published=post.published)

    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)  # update new_post with id generated in the database
    return new_post


@app.get("/posts/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id)))
    # post = cursor.fetchone()
    #post = find_post(id)

    post = db.query(models.Post).filter(models.Post.id == id).first()
    print(post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id : {id} was not found")
    return post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute(
    #     """DELETE FROM posts WHERE id = %s RETURNING * """, (str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    # index = find_index_post(id)

    post_query = db.query(models.Post).filter(models.Post.id == id)

    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id : {id} does not exist")
    post_query.delete(synchronize_session=False)
    db.commit()

    # my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute("""UPDATE posts  SET title=%s, content=%s, published=%s, rating=%s WHERE id=%s RETURNING * """,
    #                (post.title, post.content, post.published, post.rating, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    #index = find_index_post(id)

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id : {id} does not exist")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    # post_dict = post.dict()
    # post_dict["id"] = id
    #my_posts[index] = post_dict
    return post_query.first()


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
