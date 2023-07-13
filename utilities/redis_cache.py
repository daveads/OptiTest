import redis

def check_redis_connection():
    try:
        pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
        redis_conn = redis.Redis(connection_pool=pool)
        return redis_conn.ping()
    
    except redis.exceptions.ConnectionError:
        return False

def setkey(key, value):
    if check_redis_connection():
        redis_conn = redis.Redis()

        if not redis_conn.exists(key):
            redis_conn.set(key, value)
            return redis_conn.get(key).decode('utf-8')
        else:
            #print("exist")
            return redis_conn.get(key).decode('utf-8')

    else:
        return None
