"""
@File : story_schemas.py
@Date : 2023/6/14 16:57
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""
from datetime import date

from pydantic import BaseModel
from typing import Optional, Union


# 查询需求参数
class QueryStory(BaseModel):
    product: Optional[int]
    status: Optional[str]
    owner: Optional[str]
    begin: Union[str, date] = date.today()
    end: Union[str, date] = date.today()

    class Config:
        schema_extra = {
            "example": {
                "product": 0,
                "owner": "",
                "begin": "2023-06-01",
                "end": "2023-06-12",
                "status": ""
            }
        }


# 查询项目需求信息
class QueryProjectStory(BaseModel):
    product: int
    story: int
    project: Optional[int]
    version: Optional[int]

    class Config:
        schema_extra = {
            "example": {
                "product": 7,
                "story": 740,
                "project": 0,
                "version": 0,

            }
        }


if __name__ == "__main__":
    pass
