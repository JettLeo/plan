"""
第4天练习：异步编程实战 —— 串行 vs 并发
"""

import asyncio
import time
import httpx

# ============================================================
# 模拟一个耗时操作（不用真实网络请求）
# ============================================================

async def fake_network_request(url:str, delay:int=1):
    print(f"开始请求: {url}")
    await asyncio.sleep(delay)  # 模拟网络延迟
    print(f"完成请求: {url}")
    return f"响应内容来自 {url}"


# ============================================================
# 串行版本：一个一个来
# ============================================================

async def fetch_serial():
    """串行执行：总耗时 = 所有任务耗时之和"""
    print("\n=== 串行执行（逐个等待）===")
    start = time.time()

    result1 = await fake_network_request("任务1",1)
    result2 = await fake_network_request("任务2",2)
    result3 = await fake_network_request("任务3",3)

    end = time.time()
    print(f"串行执行总耗时: {end - start:.2f} 秒")
    return [result1, result2, result3]


# ============================================================
# 并发版本：同时出发
# ============================================================

async def fetch_concurrent():
    """并发执行：总耗时 = 最慢任务耗时"""
    print("\n=== 并发执行（同时发起请求）===")
    start = time.time()

    # 创建任务列表
    tasks = [
        asyncio.create_task(fake_network_request("任务1",1)),
        asyncio.create_task(fake_network_request("任务2",2)),
        asyncio.create_task(fake_network_request("任务3",3)),
    ]

    # 等待所有任务完成
    results = await asyncio.gather(*tasks)

    end = time.time()
    print(f"并发执行总耗时: {end - start:.2f} 秒")
    return results

if __name__ == "__main__":
    # 运行串行版本
    asyncio.run(fetch_serial())

    # 运行并发版本
    asyncio.run(fetch_concurrent())