import redis
from database.config import redis_port, redis_host

r = redis.Redis(host=redis_host, port=redis_port)
