from pydantic import BaseModel

class BlogSchema(BaseModel):
    title: str
    body: str
    user_id: int
