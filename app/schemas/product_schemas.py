"""
@File : product_schemas.py
@Date : 2021/11/23 14:37
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""

from pydantic import BaseModel
from typing import Optional


class Product(BaseModel):
	pass

	class Config:
		pass


class ProductProjectMapping(BaseModel):
	product_id: Optional[int]
	product_name: Optional[str]
	project_id: Optional[int]
	project_name: Optional[str]
	project_owner: Optional[str]

	class Config:
		schema_extra = {
			"example": {
				"product_id": 0,
				"product_name": "eWordRIS",
				"project_id": 0,
				"project_name": "放射系统维护2021",
				"project_owner": "wangj"
			}
		}


if __name__ == "__main__":
	pass
