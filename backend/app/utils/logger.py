import time
from functools import wraps
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TruthLens")

def time_it(name):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            logger.info(f"Task '{name}' took {end - start:.4f} seconds")
            return result
        return wrapper
    return decorator

def time_it_async(name):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start = time.time()
            result = await func(*args, **kwargs)
            end = time.time()
            logger.info(f"Task '{name}' took {end - start:.4f} seconds")
            return result
        return wrapper
    return decorator
