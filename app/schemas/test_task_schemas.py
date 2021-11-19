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
	desc: Optional[str] = ''  # TODO 这里之后要用html模板
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
				"begin": "2021-11-18",
				"end": "2021-11-18",
				"mailto": ",zyp,zl",
				"desc": "这是描述"
			}
		}


if __name__ == "__main__":
	tr = TestTask(name='xxx测试申请', product=1, project=2, build='v1.0.0.0', owner='zyp', begin='2021-11-18',
				  end='2021-11-18')
	print(tr.json())
