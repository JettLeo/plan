"""
第2天练习：装饰器
"""

import time
import random
from functools import wraps


def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"[TIMER] {func.__name__} 耗时: {elapsed:.4f}s")
        return result
    return wrapper


def retry(max_attempts=3, delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    print(f"[RETRY] {func.__name__} 第 {attempt} 次失败: {e}")
                    if attempt < max_attempts:
                        time.sleep(delay)
            raise last_exception
        return wrapper
    return decorator


def log_call(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[LOG] 调用 {func.__name__}")
        print(f"      args: {args}")
        print(f"      kwargs: {kwargs}")
        result = func(*args, **kwargs)
        print(f"      -> 返回: {result}")
        return result
    return wrapper


@timer
def slow_task():
    time.sleep(0.5)
    return "完成"


@retry(max_attempts=3, delay=0.5)
def unstable_task():
    if random.random() < 0.6:
        raise ValueError("随机失败")
    return "成功"


@log_call
def add(a, b, c=0):
    return a + b + c


if __name__ == "__main__":
    print("=== 测试 @timer ===")
    slow_task()

    print("\n=== 测试 @retry ===")
    try:
        result = unstable_task()
        print(f"最终结果: {result}")
    except Exception as e:
        print(f"全部失败: {e}")

    print("\n=== 测试 @log_call ===")
    add(1, 2, c=3)