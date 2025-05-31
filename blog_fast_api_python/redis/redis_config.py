import redis.asyncio as redis

"""
Run Redis:
    For Locally: redis-server --port 6379
    For Docker: docker run -d -p 6379:6379 --name redis-server redis
"""

# REDIS_HOST = "localhost"
REDIS_HOST = "bloggy-redis-setup-6xyih2.serverless.eun1.cache.amazonaws.com"
REDIS_PORT = 6379

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)


