# 04_fastapi_excel.py —— 第2周：接口 + Excel 导出
from fastapi import FastAPI, Body
from fastapi.responses import FileResponse
import asyncio
import time
import httpx
from openpyxl import Workbook
from typing import List

# 复用你之前的模拟请求（或者替换成真实的 httpx 请求）
async def fake_request(name: str, delay: int = 1):
    print(f"开始请求: {name}")
    await asyncio.sleep(delay)  # 模拟网络延迟
    print(f"完成请求: {name}")
    return f"响应内容来自 {name}"


app = FastAPI()

@app.post("/export_excel")
async def export_excel(tasks: List[str] = Body(...,embed=True,example=["任务1", "任务2", "任务3"]
)):
   # 2.1 并发执行爬虫
    async with httpx.AsyncClient() as client:
       task = [fake_request(name, delay=1) for name in tasks]
       results = await asyncio.gather(*task)

    # 2.2 将结果写入 Excel
    file_path = await asyncio.to_thread(write_to_excel, results)

    return FileResponse(file_path, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', filename="爬虫结果.xlsx")

def write_to_excel(data: List[str], filename: str = None):
    if filename is None:
        filename = f"爬虫结果_{int(time.time())}.xlsx"

    wb = Workbook()
    ws = wb.active
    ws.title = "爬虫结果"
    ws.append(["任务名称", "响应内容"])  # 添加表头
    for i, item in enumerate(data):
        ws[f"A{i+1}"] = item
    wb.save(filename)
    print(f"Excel 文件已保存: {filename}")
    return filename