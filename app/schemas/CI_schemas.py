"""
@File : CI_schemas.py
@Date : 2022/4/15 16:20
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""
from pydantic import BaseModel
from ipaddress import IPv4Address
from typing import Optional

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


class AddServer(BaseModel):
	ipAddress: IPv4Address
	serverName: str
	remark: Optional[str]

	# deleted: str

	class Config:
		schema_extra = {
			"example": {
				"ipAddress": "192.168.1.18",
				"serverName": "测试服务器",
				"remark": "功能测试部署应用"
			}
		}


class Server(AddServer):
	id: str
	# deleted: str

	class Config:
		schema_extra = {
			"example": {
				"id": "1",
				"ipAddress": "192.168.1.18",
				"serverName": "测试服务器1",
				"remark": "功能测试部署应用1"
			}
		}

if __name__ == "__main__":
	pass
