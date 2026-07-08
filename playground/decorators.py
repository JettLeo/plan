import time
import random
import asyncio
from functools import wraps

# ============================================================
# 装饰器 1：@timer —— 打印函数执行耗时
# ============================================================
def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Function '{func.__name__}' executed in {end_time - start_time:.4f} seconds.")
        return result
    return wrapper

# ============================================================
# 装饰器 2：@retry —— 失败自动重试
# ============================================================
def retry(max_retries=3, delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"Attempt {attempt + 1} failed: {e}")
                    if attempt < max_retries - 1:
                        time.sleep(delay)
                    else:
                        raise
        return wrapper
    return decorator

# ============================================================
# 异步装饰器（用于 async def 函数）
# ============================================================

def timer_async(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        result = await func(*args, **kwargs)
        end_time = time.time()
        print(f"Async function '{func.__name__}' executed in {end_time - start_time:.4f} seconds.")
        return result
    return wrapper    

def retry_async(max_retries=3, delay=1):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"Attempt {attempt + 1} failed: {e}")
                    if attempt < max_retries - 1:
                        await asyncio.sleep(delay)
                    else:
                        raise
        return wrapper
    return decorator

# ============================================================
# 通用装饰器（自动判断同步/异步，推荐使用）
# ============================================================

# def timer(func):
#     if asyncio.iscoroutinefunction(func):
#         return timer_async(func)
#     else:
#         return timer_sync(func)

# def retry(max_attempts=3, delay=1):
#     def decorator(func):
#         if asyncio.iscoroutinefunction(func):
#             return retry_async(max_attempts, delay)(func)
#         else:
#             return retry_sync(max_attempts, delay)(func)
#     return decorator