# Crear API con FastAPI 
# Ejemplo de un Blog    

from fastapi import FastAPI
from pydantic import BaseModel # validar los datos
from datetime import datetime
from uuid import uuid4 as uuid # generar id
from typing import Text, Optional  

posts = [] # lista de posts

class Post(BaseModel): 
  id: Optional[str]
  title: str
  author: str
  context: Text
  created_at: datetime = datetime.now()
  published_at: Optional[datetime] 
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
  posts.append(post.dict())
  return {'message': 'Post created successfully', 'post': post}

