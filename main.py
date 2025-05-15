# Crear API con FastAPI 
# Ejemplo de un Blog    

from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from uuid import uuid4 as uuid
from typing import Text, Optional

posts = [] # lista de posts

class Post(BaseModel):
    id: Optional[str] = None  # Para que Pydantic pueda generar el ID al crear
    title: str
    author: str
    context: Text
    created_at: datetime = datetime.now()
    published_at: Optional[datetime] = None
    published: bool = False

app = FastAPI()

@app.get('/')
def read_root():
    return {'Welcome': 'this is a blog'}

@app.get('/posts')
def get_posts():
    return posts

@app.post('/posts/create')
def create_post(post: Post):
    post.id = str(uuid())
    posts.append(post.model_dump())  # Usar model_dump() en lugar de dict()
    return {'message': 'Post created successfully', 'post': post}

# Ejemplo para obtener un post por ID (opcional)
@app.get('/posts/{post_id}')
def get_post(post_id: str):
    for post in posts:
        if post['id'] == post_id:
            return post
    return {'error': 'Post not found'}

