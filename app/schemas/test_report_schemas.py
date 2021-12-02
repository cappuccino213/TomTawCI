"""
@File : test_report_schemas.py
@Date : 2021/10/9 16:28
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""

from pydantic import BaseModel
from typing import Optional, Union
from datetime import date


# 常用的用于数据接口schema定义与检查的库
# 用法介绍：https://cloud.tencent.com/developer/article/1806545


class TestReport(BaseModel):
	id: Optional[int]  # 新增时id不用填写
	deleted: Optional[str] = '0'
	createdBy: str
	createdDate: Optional[str]  # 新增时创建时间不需要填写,默认为当前时间
	product: int
	project: int
	tasks: str
	builds: str
	title: str
	begin: Union[str, date]  # 同时支持str,date类型
	end: Union[str, date]
	owner: str
	members: Optional[str] = ''  # 因为数据库定义中为非空，故赋予空字符串
	stories: Optional[str] = ''
	bugs: Optional[str] = ''
	cases: Optional[str] = ''
	report: Optional[str] = ''
	objectType: Optional[str] = 'testtask'
	objectID: int

	class Config:
		schema_extra = {
			"example": {
				"id": 0,
				"createdBy": "zyp(禅道的账号)",
				"createdDate": "2021-11-19 16:03:16（不传默认为当前时间）",
				"product": 2,
				"project": 1,
				"tasks": "666(测试单)",
				"builds": "888(版本id)",
				"title": "测试报告名称",
				"begin": "2021-11-18(测试开始时间)",
				"end": "2021-11-18(测试结束时间)",
				"owner": "zyp(责任人)",
				"members": "参与测试的人员（多个以逗号隔开）",
				"stories": "关联的需求号（多个以逗号隔开）",
				"bugs": "关联的bug号（多个以逗号隔开）",
				"cases": "关联的测试用例号（多个以逗号隔开）",
				"report": "测试总结",
				"objectType": "testtask",
				"objectID": 666
			}
		}


class AutoTestReport(BaseModel):
	task_id: int
	test_time: Optional[str]
	test_url: Optional[str]
	test_client: Optional[str]
	test_tool: Optional[str]
	test_content: Optional[str]
	risk_evaluation: Optional[str]
	summary: Optional[str]

	class Config:
		schema_extra = {
			"example": {
				"task_id": 0,
				"test_time": "1MD(测试耗时)",
				"test_url": "test.ris.com(测试地址)",
				"test_client": "Win10 PRO(测试客户机的环境情况)",
				"test_tool": "DevTool、F12（测试过程中使用的工具）",
				"test_content": "测试内容",
				"risk_evaluation": "风险评估",
				"summary": "测试总结"
			}
		}


if __name__ == "__main__":
	pass
