from pydantic import BaseModel

class AdminUserSchema(BaseModel):
    first_name: str
    last_name: str
    email: str
    username: str
    password: str

class UserSchema(BaseModel):
    first_name: str
    last_name: str
    email: str
    username: str
    password: str

class UpdateUserSchema(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
    
class LoginRequest(BaseModel):
    email: str
    password: str
