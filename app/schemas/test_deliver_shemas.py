"""
@File : test_deliver_shemas.py
@Date : 2021/11/24 9:25
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""
from pydantic import BaseModel
from typing import Optional


class Deliver(BaseModel):
	# 版本相关
	product_id: int
	product_name: str
	old_build_id: int
	new_build_name: str
	builder: str
	desc: str
	scmPath: Optional[str]
	filePath: Optional[str]
	# 测试单相关
	project_id: int
	project_name: str
	if_smoke: str
	man_time: str
	owner: str
	mailto: str
	test_type: str
	test_suggest: str

	class Config:
		schema_extra = {
			"example": {
				"product_id": 0,
				"product_name": "产品名称",
				"project_id": 0,
				"project_name": "项目名称",
				"if_smoke": "是/否",
				"man_time": "1MD/2MH(工日或工时)",
				"old_build_id": 0,
				"new_build_name": "v1.0.0.0(版本名称)",
				"builder": "wangj",
				"desc": "版本信息描述",
				"scmPath": r"\\192.168.1.19\delivery\eWordRIS\V2.2.0.4286.20211117（源码路径，可选）",
				"filePath": r"\\192.168.1.19\delivery\eWordRIS\V2.2.0.4286.20211117（文件路径，可选）",
				"owner": "zyp",
				"mailto": ",zyp,zhangl(多个用户用,隔开，首个字符也是,)",
				"test_type": "功能/接口/BUG回归等",
				"test_suggest": "测试建议(1、参考文档2、注意事项3、测试着重点 等其他说明)"
			}
		}


if __name__ == "__main__":
	pass
