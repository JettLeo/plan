"""
学习专用 FastAPI 服务
用于测试 Pydantic 模型、装饰器、异步等功能
"""
import os
import random
import asyncio
from fastapi import FastAPI
from playground.pydantic_models import ImportRequest
from playground.decorators import timer_async, retry
from dotenv import load_dotenv

load_dotenv()  # 加载 .env 文件中的环境变量


# 从环境变量读取配置，如果不存在则使用默认值
HOST = os.getenv("APP_HOST", "127.0.0.1")
PORT = int(os.getenv("APP_PORT", "8001"))
RELOAD = os.getenv("APP_RELOAD", "true").lower() == "true"


app = FastAPI(title="学习专用 FastAPI 服务", description="用于测试 Pydantic 模型、装饰器、异步等功能", version="1.0.0")

# ============================================================
# 测试接口 1：Pydantic 模型 + @timer
# ============================================================

@app.post("/test-import")
@timer_async
async def test_import(import_request: ImportRequest):
    # 模拟一些异步操作
    await asyncio.sleep(1)
    return {"message": "Import successful", "data": import_request}

# ============================================================
# 测试接口 2：@retry 重试机制
# ============================================================

@retry(max_retries=5, delay=2)
async def unreliable_function():
    if random.random() < 0.7:  # 70% 概率失败
        raise ValueError("Simulated failure")
    return "Success!"

@app.get("/test-retry")
async def test_retry():
    try:
        result = unreliable_function()
        return {"success": True, "data": result}
    except Exception as e:
        return {"success": False, "error": str(e)}
    
# ============================================================
# 测试接口 3：纯健康检查
# ============================================================    
@app.get("/")
async def root():
    return {"message": "服务运行正常", "status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host=HOST,
        port=PORT,
        reload=RELOAD
    )