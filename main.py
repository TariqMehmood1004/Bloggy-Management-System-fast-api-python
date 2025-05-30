from fastapi import FastAPI
from .database.database import engine
from .routes.blogs.blogs_route import router as blogs_router
from .routes.users.users_route import router as users_router

app = FastAPI()

# Create all tables
from . import models
models.Base.metadata.create_all(bind=engine)

# Include routes
app.include_router(users_router)
app.include_router(blogs_router)
