"""
@File : CI_schemas.py
@Date : 2022/4/15 16:20
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""
from pydantic import BaseModel
from ipaddress import IPv4Address

"""服务器检测"""


class ServerCheck(BaseModel):
	ip_list: list[IPv4Address]

	class Config:
		schema_extra = {
			"example": {
				"ip_list": ['192.168.1.2', '192.168.1.5', '192.168.1.6', '192.168.1.7', '192.168.1.8', '192.168.1.9',
							'192.168.1.11']
			}
		}


if __name__ == "__main__":
	pass
