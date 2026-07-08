# 04_fastapi_excel.py —— 真实爬虫版（已加限流）
from fastapi import FastAPI, Body
from fastapi.responses import FileResponse
import asyncio
import time
import httpx  # ★ 重新导入 httpx（之前删了，现在要加回来）
from openpyxl import Workbook
from typing import List
import logging

# ★ 新函数：真实的异步 HTTP 请求（替代 fake_request)
async def real_fetch(client: httpx.AsyncClient, url: str):
    try:
        response = await client.get(url, timeout=10.0)
        response.raise_for_status()  # 如果响应状态码不是 2xx，会抛出异常
        return response.text
    except httpx.RequestError as e:
        logging.info(f"请求错误: {e}")
        return f"请求错误: {e}"
    except httpx.HTTPStatusError as e:
        print(f"HTTP 错误: {e.response.status_code} - {e.response.text}")
        return f"HTTP 错误: {e.response.status_code} - {e.response.text}"
    
app = FastAPI()

@app.post("/export_excel")
async def export_excel(urls: List[str] = Body(..., embed=True, example=["https://www.baidu.com", 
        "https://www.zhihu.com", 
        "https://www.bilibili.com",
        "https://www.csdn.net",
        "https://www.163.com",
        "https://www.sina.com.cn"])):
     # ★ 限流器：同时最多 3 个请求（真实爬虫建议 3~5）
    semaphore = asyncio.Semaphore(3)

    # ★ 内部函数：带上信号量 + 复用 client 连接池
    async def limited_fetch(client: httpx.AsyncClient, url: str):
        async with semaphore:
            return await real_fetch(client, url)
        
    # ★ 使用 async with 管理连接池（对标 Java try-with-resources）
    # ★ 修改后（加上伪装请求头）
    async with httpx.AsyncClient(
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        }
    ) as client:
        tasks = [limited_fetch(client, url) for url in urls]
        results = await asyncio.gather(*tasks)

    # 后续：写入 Excel + 返回文件（完全不动
    file_path = await asyncio.to_thread(write_to_excel, results)

    return FileResponse(file_path, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', filename="爬虫结果.xlsx")

def write_to_excel(data: List[str], filename: str = None):
    if filename is None:
        filename = f"爬虫结果_{int(time.time())}.xlsx"

    wb = Workbook()
    ws = wb.active
    ws.title = "爬虫结果"
    ws.append(["URL抓取结果"])  # 表头简化

    for idx,item in enumerate(data):
        ws.append([f"{idx}. {item}"])  # 每行写入一个结果

    wb.save(filename)
    print(f"Excel 文件已保存: {filename}")
    return filename    