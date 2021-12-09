"""
@File : build_schemas.py
@Date : 2021/11/19 14:53
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""
from pydantic import BaseModel
from typing import Optional,Union
from datetime import date


class Build(BaseModel):
	id: Optional[int]
	name: str
	branch: Optional[str] = 0
	product: int
	project: int
	scmPath: Optional[str]
	filePath: Optional[str]
	# date: Optional[str] = date.today()
	date: Union[str,date]
	stories: Optional[str] = ''
	bugs: Optional[str] = ''
	builder: str
	desc: str
	deleted: str = '0'

	class Config:
		schema_extra = {
			"example": {
				"name": "V2.2.0.4400",
				"product": 1,
				"project": 2,
				"builder": "zyp(禅道的账号)",
				"scmPath": r"\\192.168.1.19\delivery\eWordRIS\V2.2.0.4286.20211117",
				"filePath": r"\\192.168.1.19\delivery\eWordRIS\V2.2.0.4286.20211117",
				"date": "2021-11-18",
				"desc": "1.新增xxxx模块 2.优化xxxx功能 3.修复xxxx问题 4.完成xxxx需求"
			}
		}


class QueryBuild(BaseModel):
	product: Optional[int]
	project: Optional[int]
	name: Optional[str]

	class Config:
		schema_extra = {
			"example": {
				"name": "v1.1.1.1232",
				"product": 7,
				"project": 66
			}
		}


if __name__ == "__main__":
	qbs = QueryBuild(product=1,project=2)
	qbs.name='222'
	print(qbs.dict())
