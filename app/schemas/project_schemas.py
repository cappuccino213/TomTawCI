"""
@File : project_schemas.py
@Date : 2023/6/30 15:08
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""
from datetime import date
from pydantic import BaseModel
from typing import Optional, Union


# 查询项目列表
class QueryProject(BaseModel):
    type: Optional[str]
    code: Optional[str]
    status: Optional[str]
    Leader: Optional[str]
    createUser: Optional[str]
    begin: Union[str, date] = date.today()
    end: Union[str, date] = date.today()
    product: Optional[int]


    class Config:
        schema_extra = {
            "example": {
                "type": "",
                "code": "",
                "status":"",
                "Leader": "",
                "createUser": "",
                "begin": "2023-01-01",
                "end": "2023-12-31",
                "product": 0
            }
        }


if __name__ == "__main__":
    pass
