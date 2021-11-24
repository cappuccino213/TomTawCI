"""
@File : user_schemas.py
@Date : 2021/11/24 14:06
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""
from pydantic import BaseModel
from typing import Optional, Union


class User(BaseModel):
	account: Optional[str]
	dept: Optional[str]
	role: Optional[str]
	gender: Optional[str]

	# 内部类，固定用法，声明请求示例
	class Config:
		schema_extra = {
			"example": {
				"account": "wangj（用户名，可选）",
				"dept": "3(部门编码，3:研发、4:测试，可选)",
				"role": "dev（角色编码，dev:研发、qa：测试，可选）",
				"gender": "m/f(性别编码，可选)"
			}
		}


if __name__ == "__main__":
	pass
