from pydantic import BaseModel

class UserSchema(BaseModel):
    first_name: str
    last_name: str
    email: str
    username: str
    password: str
    is_admin: bool = False


class UpdateUserSchema(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
    
class LoginRequest(BaseModel):
    email: str
    password: str
