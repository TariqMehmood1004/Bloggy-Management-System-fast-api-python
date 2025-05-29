from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


DATABASE_URL = "postgresql://blogFastAPIdb_owner:npg_08ovskEXLxSa@ep-icy-king-a8jldnnt-pooler.eastus2.azure.neon.tech/blogFastAPIdb?sslmode=require"


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
