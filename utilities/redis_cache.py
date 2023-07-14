import redis


class CacheError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


def check_redis_connection():
    """
    Check the connection to the Redis server.

    Returns:
        bool: True if the connection is successful, False otherwise.
    """
    try:
        pool = redis.ConnectionPool(host="localhost", port=6379, db=0)
        redis_conn = redis.Redis(connection_pool=pool)
        return redis_conn.ping()

    except redis.exceptions.ConnectionError as e:
        raise CacheError("Redis connection error occurred.") from e


def setkey(key, value):
    """
    Set a key-value pair in Redis cache.

    Args:
        key (str): The key to set.
        value (str): The value to set for the key.

    Returns:
        str: The value of the key in Redis cache, or None if the connection fails.
    """
    try:
        if check_redis_connection():
            redis_conn = redis.Redis()

            if not redis_conn.exists(key):
                redis_conn.set(key, value)
                return redis_conn.get(key).decode("utf-8")
            else:
                return redis_conn.get(key).decode("utf-8")
        else:
            raise CacheError("Failed to connect to Redis server.")

    except redis.exceptions.RedisError as e:
        raise CacheError("Redis error occurred.") from e
