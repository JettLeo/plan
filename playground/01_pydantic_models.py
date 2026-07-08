"""
第1天练习：Pydantic 模型定义 + 类型注解
"""

from typing import Optional, List
from pydantic import BaseModel, field_validator


class SubTableRow(BaseModel):
    check_list: str
    check_name: str
    unit: Optional[str] = None
    design_value: Optional[float] = None
    measured_values: List[float] = []

    @field_validator("check_list")
    @classmethod
    def check_list_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("check_list 不能为空")
        return v.strip()


class MainTable(BaseModel):
    project_name: str
    fill_date: str
    filler: Optional[str] = None
    contract_no: Optional[str] = None


class ImportRequest(BaseModel):
    table_id: str
    lib_name: str
    main: MainTable
    sub_rows: List[SubTableRow] = []


if __name__ == "__main__":
    # 测试数据
    req = ImportRequest(
        table_id="test_001",
        lib_name="test_lib",
        main=MainTable(
            project_name="测试项目",
            fill_date="2026-06-30",
            filler="张三"
        ),
        sub_rows=[
            SubTableRow(
                check_list="7.1",
                check_name="压实度",
                unit="%",
                design_value=95.0,
                measured_values=[96.5, 97.0, 94.5]
            )
        ]
    )
    print(req.model_dump_json(indent=2))