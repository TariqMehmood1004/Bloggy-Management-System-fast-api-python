from fastapi import FastAPI, Depends
from fastapi import Response, Request, Security, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from .database.database import SessionLocal, engine
from .models.blog import Blog as BlogModel
from .models.user import User as UserModel
from .models.token import Token as TokenModel
from .schemas.blog_schema import BlogSchema
from .schemas.user_schema import UserSchema, LoginRequest

from .utils.hash import hash_password
from .utils.api_response_handler import APIResponse
from .utils.catch_exception import catch_exception

from .auth.jwt_handler import create_access_token
from .redis.redis_config import redis_client
from .config.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from uuid import UUID



app = FastAPI()

# Create tables
from . import models
models.Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


@app.get("/users/me", response_model=UserSchema)
def get_current_user(
    token: str = Security(oauth2_scheme),
    db: Session = Depends(get_db)
    ):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    print("Received JWT token:", token)

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        print("Decoded JWT payload:", payload)

        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        user_id = UUID(user_id)
    except (JWTError, ValueError):
        raise credentials_exception

    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if user is None:
        raise credentials_exception

    return user.to_dict()


# register user
@app.post("/register")
@catch_exception
async def create_user(user: UserSchema, db: Session = Depends(get_db)):
    new_data = UserModel(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        username=user.username,
        password=hash_password(user.password)
    )
    
    db.add(new_data)
    db.commit()
    db.refresh(new_data)
    
    return APIResponse.HTTP_201_CREATED(data=user.dict(), message="User created successfully")


# login username, password
@app.post("/login")
@catch_exception
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    username = form_data.username
    password = form_data.password

    user = db.query(UserModel).filter(UserModel.username == username).first()
    if not user:
        return APIResponse.HTTP_404_NOT_FOUND(message="User not found")

    if not user.verify_password(password):
        return APIResponse.HTTP_401_UNAUTHORIZED(message="Invalid credentials")

    access_token = create_access_token(data={"sub": str(user.id)})

    # Save token in DB
    token_entry = TokenModel(
        user_id=user.id,
        token=access_token
    )
    db.add(token_entry)
    db.commit()

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

# Users
@app.get("/users")
@catch_exception
async def get_users(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
    ):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    print("Received JWT token on get_users:", token)

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("Decoded JWT payload:", payload)

        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        user_id = UUID(user_id)
    except (JWTError, ValueError):
        raise credentials_exception

    users = db.query(UserModel).all()
    return APIResponse.HTTP_200_OK(
        data=[u.to_dict() for u in users], 
        message="Users fetched successfully")


### --------

# Caching utility
def get_cached_blogs():
    cached = redis_client.get("blogs")
    if cached:
        return json.loads(cached)
    return None

def set_cached_blogs(data):
    redis_client.setex("blogs", 60, json.dumps(data))  # Cache for 60 seconds
    
### --------

@app.get("/blogs")
@catch_exception
async def get_blogs(db: Session = Depends(get_db)):
    blogs = db.query(BlogModel).all()
    
    if not blogs:
        return APIResponse.HTTP_404_NOT_FOUND(message="No blogs found")
    
    data = [b.to_dict() for b in blogs]
    
    return APIResponse.HTTP_200_OK(data=data, message="Blogs fetched successfully")


@app.post("/blogs")
@catch_exception
async def create_blog(blog: BlogSchema, db: Session = Depends(get_db)):
    new_blog = BlogModel(**blog.dict())
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return APIResponse.HTTP_201_CREATED(data=blog.dict(), message="Blog created successfully")


