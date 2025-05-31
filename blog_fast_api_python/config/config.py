from dotenv import load_dotenv
import os

load_dotenv()

# JWT Config
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

# import secrets
# secret_key = secrets.token_urlsafe(64)
# print(secret_key)