# Crear un CRUD API con FastAPI 
# Ejemplo de un Blog    

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from uuid import uuid4 as uuid
from typing import Text, Optional

posts = [] # lista de posts
# create a list of 2 posts
posts.append({
    'id': str(uuid()),
    'title': 'Post 1',
    'author': 'Author 1',
    'context': 'This is the context of post 1',
    'created_at': datetime.now(),
    'published_at': None,
    'published': False
})

posts.append({
    'id': str(uuid()),
    'title': 'Post 2',
    'author': 'Author 2',
    'context': 'This is the context of post 2',
    'created_at': datetime.now(),
    'published_at': None,
    'published': False
})


# Define models
# Pydantic is a ORM (Object Relational Mapper) for Python
class Post(BaseModel):
    id: Optional[str] = None  # Para que Pydantic pueda generar el ID al crear
    title: str
    author: str
    context: Text
    created_at: datetime = datetime.now()
    published_at: Optional[datetime] = None
    published: bool = False

class PostUpdate(BaseModel): # Esto es para simular la eliminacion de en registro en BD
    title: str
    author: str
    context: Text

app = FastAPI()

@app.get('/')
def read_root():
    return {'Welcome back': 'this is a blog'}

# Get all Posts
@app.get('/posts')
def get_posts():
    return posts


# Get a Post by ID 
@app.get('/posts/{post_id}')
def get_post(post_id: str):
    for post in posts:
        if post['id'] == post_id:
            return post
    # return {'error': 'Post not found'}
    raise HTTPException(status_code=404, detail="Post not found")

# Create a Post
@app.post('/posts/create')
def create_post(post: Post):
    post.id = str(uuid())
    posts.append(post.model_dump())  # Usar model_dump() en lugar de dict()
    return {'message': 'Post created successfully', 'post': post}

# Delete a Post  OJO: esto es asi pk se trata de un Array, para una BD es diferente.
@app.delete('/posts/delete/{post_id}')
def delete_post(post_id: str):
    for index, post in enumerate(posts): # Enumerate to get index
        if post['id'] == post_id:        # compare id
            posts.pop(index)             # delete post
            return {'message': 'Post deleted successfully', 'post': post}
    raise HTTPException(status_code=404, detail="Post not found") 

@app.put('/posts/update/{post_id}')
def update_post(post_id: str, updatedPost: PostUpdate):
    for post in posts:
        if post['id'] == post_id:
            post.update(updatedPost.model_dump())
            return {'message': 'Post updated successfully', 'post': post['id']}
    raise HTTPException(status_code=404, detail=f"Post not found {post_id}")