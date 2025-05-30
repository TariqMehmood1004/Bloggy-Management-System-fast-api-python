from pydantic import BaseModel
from uuid import UUID


class BlogSchema(BaseModel):
    title: str
    body: str
    
