from pydantic import BaseModel

class UserSchema(BaseModel):
    first_name: str
    last_name: str
    email: str
    username: str
    password: str
    is_admin: bool = False
    
    
class LoginRequest(BaseModel):
    email: str
    password: str
