from openpyxl import Workbook

wb = Workbook()
ws = wb.active
ws.append(["姓名", "年龄", "部门"])
ws.append(["张三", 28, "技术部"])
ws.append(["李四", 34, "市场部"])
ws.append(["王五", 45, "财务部"])
wb.save("sample.xlsx")
print("sample.xlsx 已创建")