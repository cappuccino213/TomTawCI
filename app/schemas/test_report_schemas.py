"""
@File : test_report_schemas.py
@Date : 2021/10/9 16:28
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# 常用的用于数据接口schema定义与检查的库
# 用法介绍：https://cloud.tencent.com/developer/article/1806545


class TestReport(BaseModel):
	id: Optional[int]  # 新增时id不用填写
	deleted: str = '0'
	createdBy: str
	createdDate: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 新增时创建时间不需要填写,默认为当前时间
	product: int
	project: int
	tasks: str
	builds: str
	title: str
	begin: str
	end: str
	owner: str
	members: str
	stories: str
	bugs: str
	cases: str
	report: str
	objectType: str
	objectID: int


class TestReportCreate(TestReport):
	pass


class TestReportUpdate(TestReport):
	id: int


if __name__ == "__main__":
	pass
