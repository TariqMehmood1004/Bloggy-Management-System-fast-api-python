import redis.asyncio as redis
from dotenv import load_dotenv
import os


load_dotenv()


REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")


redis_client = redis.Redis(host=REDIS_HOST, port=int(REDIS_PORT), decode_responses=True)


async def verify_redis_connection():
    try:
        pong = await redis_client.ping()
        print("Redis Connected:", pong)
    except Exception as e:
        print("Redis Connection Error:", e)
