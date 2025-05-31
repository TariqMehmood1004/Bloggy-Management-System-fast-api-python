from fastapi import FastAPI
from blog_fast_api_python.database.database import engine
from blog_fast_api_python.routes.blogs.blogs_route import router as blogs_router
from blog_fast_api_python.routes.users.users_route import router as users_router
from blog_fast_api_python.redis.redis_config import redis_client


app = FastAPI()


# Create all tables
from . import models
models.Base.metadata.create_all(bind=engine)

@app.on_event("startup")
async def test_redis():
    try:
        await redis_client.set("startup_check", "ok")
        val = await redis_client.get("startup_check")
        print("Redis connected:", val)
    except Exception as e:
        print("Redis connection failed:", e)


# Include routes
app.include_router(users_router)
app.include_router(blogs_router)
