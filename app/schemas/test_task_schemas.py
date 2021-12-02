"""
@File : test_task_schemas.py
@Date : 2021/11/18 17:15
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""
from pydantic import BaseModel
from typing import Optional, Union
from datetime import date


class TestTask(BaseModel):
	id: Optional[int]  # 新增时可以不用传，自增字段
	name: str
	product: int
	project: int
	build: str
	owner: str
	pri: Optional[int] = 2
	begin: Union[str, date] = date.today()  # 可选类型
	end: Union[str, date] = date.today()
	mailto: Optional[str]
	desc: Optional[str] = ''
	status: str = 'wait'  # 枚举值'blocked'（阻塞）, 'doing'（进行中）, 'wait'(未开始), 'done'（完成）
	deleted: str = '0'

	# 内部类，固定用法，声明请求示例
	class Config:
		schema_extra = {
			"example": {
				"name": "xxx测试申请",
				"product": 1,
				"project": 2,
				"build": "v1.0.0.0",
				"owner": "zyp",
				"pri": 2,
				"begin": "2021-11-18（一定要传值，不然默认为当天）", #
				"end": "2021-11-18（一定要传值，不然默认为当天）",
				"mailto": ",zyp,zl",
				"desc": "这是描述"
			}
		}


class TestTaskWithoutReport1(BaseModel):
	id: Optional[int] = 0
	product: Optional[int] = 0
	project: Optional[int] = 0
	owner: Optional[str] = None

	class Config:
		schema_extra = {
			"example": {
				"id": 0,
				"product": 0,
				"project": 0,
				"owner": "zyp",
			}
		}


class TestTaskWithoutReport(BaseModel):
	id: Optional[list] = None
	product: Optional[list] = None
	project: Optional[list] = None
	owner: Optional[str] = None

	class Config:
		schema_extra = {
			"example": {
				"id": [],
				"product": [],
				"project": [],
				"owner": "zyp",
			}
		}


if __name__ == "__main__":
	tr = TestTask(name='xxx测试申请', product=1, project=2, build='v1.0.0.0', owner='zyp', begin='2021-11-18',
				  end='2021-11-18')
	print(tr.json())
