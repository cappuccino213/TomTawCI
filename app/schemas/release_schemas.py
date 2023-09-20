"""
@File : release_schemas.py
@Date : 2021/11/29 17:02
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""
from pydantic import BaseModel
from typing import Optional


class CreateRelease(BaseModel):
	# name: product_name+build_name+发布类型+发布日期
	product: int
	product_name: str
	product_code: str
	project: int
	build: int
	build_name: str
	release_type: str = 'RTX'  # 改成枚举类型,M、RTX、RC、Beta
	marker: Optional[str]
	# date: Optional[str]
	apply_scope: str = '通用'  # OEM
	release_content: str = '程序包'
	ChangeLog_url: str  # changelog链接
	update_note: str  # 更新说明
	attention: str  # 注意事项
	release_link: str = ''  # 发布链接
	# members: str  # 相关人员
	members: list[dict]  # 相关人员
	releaser: str  # 发布人
	compress_secret:str # 压缩密码

	# desc: 发布版本号、适用范围、发布内容

	class Config:
		schema_extra = {
			"example": {
				"product": 7,
				"product_name": "产品名称",
				"product_code": "产品代码",
				"project": 66,
				"build": 642,
				"build_name": "V2.2.0.4083",
				"release_type": "发布类型（M:里程碑版本，RTX：正式版本，RC：预发布版本，Beta：测试发布版本）",
				"marker": "0(0,1是否为里程碑版本)",
				# "date": "yyyy-mm-dd（发布日期可选，默认为当天）",
				"apply_scope": "适用范围（通用、OEM）",
				"release_content": "发布内容",
				"ChangeLog_url": "changlog的链接",
				"update_note": "更新说明的链接",
				"attention": "注意事项，html格式",
				"release_link": "发布链接，html格式",
				"compress_secret": "压缩密码",
				"members": [
					{
						"project": 66,
						"role": "UI设计",
						"account": "dengx",
						"name": "邓旋",
						"email": "17364532478@163.com"
					},
					{
						"project": 66,
						"role": "研发主管",
						"account": "hdh",
						"name": "胡东慧",
						"email": "821469475@qq.com"
					},
					{
						"project": 66,
						"role": "研发",
						"account": "lpl",
						"name": "李鹏龙",
						"email": "571337861@qq.com"
					},
					{
						"project": 66,
						"role": "研发",
						"account": "ouj",
						"name": "欧进",
						"email": "945538629@qq.com"
					},
					{
						"project": 66,
						"role": "研发主管",
						"account": "wangj",
						"name": "王晶",
						"email": "526856808@qq.com"
					},
					{
						"project": 66,
						"role": "测试负责人",
						"account": "zyp",
						"name": "张烨平",
						"email": "1483029082@qq.com"
					}
				],
				"releaser": "发布人员（当前登录人员）"
			}
		}


if __name__ == "__main__":
	pass
