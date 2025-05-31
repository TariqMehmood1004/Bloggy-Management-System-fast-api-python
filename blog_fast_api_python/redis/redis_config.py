import redis.asyncio as redis

"""
Run Redis:
    For Locally: redis-server --port 6380
    For Docker: docker run -d -p 6380:6380 --name redis-server redis
"""

REDIS_HOST = "localhost"
REDIS_PORT = 6380

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)


