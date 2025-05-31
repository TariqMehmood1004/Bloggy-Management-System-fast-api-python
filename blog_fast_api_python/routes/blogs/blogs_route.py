from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ...models.blog import Blog as BlogModel
from ...models.user import User as UserModel
from ...schemas.blog_schema import BlogSchema
from ...utils.api_response_handler import APIResponse
from ...utils.catch_exception import catch_exception
from ...database.database import get_db
from ...redis.redis_config import redis_client
from fastapi.security import OAuth2PasswordBearer
from ...config.config import SECRET_KEY, ALGORITHM
from uuid import UUID
from jose import jwt
from fastapi import Security
from sqlalchemy import desc
from datetime import datetime
import json


# Router
router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")



# --------------------------------

# Create Blog
@router.post("/blogs")
@catch_exception
async def create_blog(
    blog: BlogSchema,
    token: str = Security(oauth2_scheme),
    db: Session = Depends(get_db)
    ):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    user_id = UUID(payload.get("sub"))

    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        return APIResponse.HTTP_404_NOT_FOUND(message="User not found")

    print(f"User ID: {user_id}")

    new_blog = BlogModel(
        title=blog.title,
        body=blog.body,
        user_id=user.id
    )

    if not new_blog:
        return APIResponse.HTTP_404_NOT_FOUND(message="Blog not created")

    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    # Invalidate Redis cache for blog listing
    await redis_client.delete("blogs_cache")

    return APIResponse.HTTP_201_CREATED(data=new_blog.to_dict(), message="Blog created successfully")


# Get All Blogs | Read all the blogs | Caching
@router.get("/blogs")
@catch_exception
async def get_blogs(db: Session = Depends(get_db)):
    cache_key = "blogs_cache"
    
    # Try to get cached blogs
    cached_data = await redis_client.get(cache_key)
    if cached_data:
        blogs = json.loads(cached_data)
        return APIResponse.HTTP_200_OK(data=blogs, message="Blogs fetched from cache")

    # If not cached, query the database
    blogs_query = db.query(BlogModel).order_by(desc(BlogModel.created_at)).all()
    if not blogs_query:
        return APIResponse.HTTP_404_NOT_FOUND(message="No blogs found")

    blogs = [b.to_dict() for b in blogs_query]

    # Cache the result with an expiration time (e.g., 300 seconds)
    cache_blog = await redis_client.set(cache_key, json.dumps(blogs), ex=300)
    print(f"Cached blogs: {cache_blog}")

    return APIResponse.HTTP_200_OK(data=blogs, message="Blogs fetched successfully")


# Delete All Blogs
@router.delete("/blogs")
@catch_exception
async def delete_all_blogs_by_authorized(
    token: str = Security(oauth2_scheme),
    db: Session = Depends(get_db)
    ):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = UUID(payload.get("sub"))
    except (JWTError, ValueError):
        return APIResponse.HTTP_401_UNAUTHORIZED(message="Could not validate credentials")

    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        return APIResponse.HTTP_404_NOT_FOUND(message="User not found")

    blogs = db.query(BlogModel).filter(BlogModel.user_id == user.id).order_by(desc(BlogModel.created_at)).all()
    if not blogs:
        return APIResponse.HTTP_404_NOT_FOUND(message="User not authorized to delete blogs.")
    
    data = [b.to_dict() for b in blogs]

    for blog in blogs:
        db.delete(blog)
    db.commit()

    # Invalidate cached blogs list
    await redis_client.delete("blogs_cache")

    return APIResponse.HTTP_200_OK(message="Blogs deleted successfully", data=data)

# Delete Blog
@router.delete("/blogs/{blog_id}")
@catch_exception
async def delete_blog_by_authorized(
    blog_id: UUID,
    token: str = Security(oauth2_scheme),
    db: Session = Depends(get_db)
    ):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = UUID(payload.get("sub"))
    except (JWTError, ValueError):
        return APIResponse.HTTP_401_UNAUTHORIZED(message="Could not validate credentials")

    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        return APIResponse.HTTP_404_NOT_FOUND(message="User not found")

    blog = db.query(BlogModel).filter(BlogModel.id == blog_id, BlogModel.user_id == user.id).first()
    if not blog:
        return APIResponse.HTTP_404_NOT_FOUND(message="Blog not found or you are not authorized to delete it")

    data = blog.to_dict()

    db.delete(blog)
    db.commit()

    return APIResponse.HTTP_200_OK(message="Blog deleted successfully", data=data)


# Update Blog
@router.put("/blogs/update/{blog_id}")
@catch_exception
async def update_blog(
    blog_id: UUID, 
    new_blog: BlogSchema, 
    token: str = Security(oauth2_scheme),
    db: Session = Depends(get_db)):
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = UUID(payload.get("sub"))
    except (JWTError, ValueError):
        return APIResponse.HTTP_401_UNAUTHORIZED(message="Could not validate credentials")

    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        return APIResponse.HTTP_404_NOT_FOUND(message="User not found")

    blog = db.query(BlogModel).filter(BlogModel.id == blog_id, BlogModel.user_id == user.id).first()
    if not blog:
        return APIResponse.HTTP_404_NOT_FOUND(message="User not authorized to update blog.")
    
    blog.title = new_blog.title
    blog.body = new_blog.body
    blog.updated_at = datetime.now()
    db.commit()
    
    return APIResponse.HTTP_200_OK(data=blog.to_dict(), message="Blog updated successfully")


# Get Blog
@router.get("/blogs/{blog_id}")
@catch_exception
async def get_blog(blog_id: UUID, db: Session = Depends(get_db)):
    blog = db.query(BlogModel).filter(BlogModel.id == blog_id).first()
    if not blog:
        return APIResponse.HTTP_404_NOT_FOUND(message="Blog not found")
    return APIResponse.HTTP_200_OK(data=blog.to_dict(), message="Blog fetched successfully")


# Current User Blogs
@router.get("/users/me/blogs")
@catch_exception
async def get_current_user_blogs(token: str = Security(oauth2_scheme), db: Session = Depends(get_db)):
    
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    user_id = UUID(payload.get("sub"))
    print(f"User ID: {user_id}")
   
    blogs = db.query(BlogModel).filter(BlogModel.user_id == user_id).order_by(desc(BlogModel.created_at)).all()
    print(f"Blogs: {blogs}")

    if not blogs:
        return APIResponse.HTTP_404_NOT_FOUND(message="No blogs found")
    
    data = [b.to_dict() for b in blogs]
    
    return APIResponse.HTTP_200_OK(data=data, message="Blogs fetched successfully")


# --------------------------------
