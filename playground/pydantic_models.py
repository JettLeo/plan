from typing import List, Optional
from pydantic import BaseModel, field_validator


#定义子项的数据结构
class SubTableRow(BaseModel):#结构体定义
    check_list: str #字段类型定义
    check_name: str
    unit: Optional[str] = None
    design_value: Optional[float] = None
    measured_values: List[float] = []   # 实测值列表

    @field_validator('check_list')
    @classmethod
    def check_list_must_not_be_empty(cls, v): #调用方法
        if not v:
            raise ValueError('check_list must not be empty')
        return v
    
class MainTable(BaseModel):
    project_name: str
    fill_date: str
    filler: str | None = None
    contract_no: str | None = None

class ImportRequest(BaseModel):
    table_id: str
    lib_name: str
    main: MainTable
    sub_rows: list[SubTableRow] = []    