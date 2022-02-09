"""
@File : CD_schemas.py
@Date : 2022/1/24 15:50
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""
from pydantic import BaseModel
from typing import Optional
from ipaddress import IPv4Address


class CDRegister(BaseModel):
	hostname: str
	ip: IPv4Address
	desc: Optional[str]
	online: bool

	class Config:
		schema_extra = {
			"example": {
				"hostname": 'DESKTOP-L7R9KAB',
				"ip": "192.168.1.56",
				"desc": "测试机",
				"online": True
			}
		}


class AppParameter(BaseModel):
	task_id: int
	service_name: str
	config_files: list[str]

	class Config:
		schema_extra = {
			"example": {
				"task_id": 726,
				"service_name": 'eWordRISAPI',
				"config_files": ['appsettings.json', 'DBConfig.json', 'log4net.config']
			}
		}


class AppUpgrade(BaseModel):
	CD_url: IPv4Address
	app_para: AppParameter


class CDClientIP(BaseModel):
	ip: IPv4Address

	class Config:
		schema_extra = {
			"example": {
				"ip": "192.168.1.18"
			}
		}


class ServiceQuery(BaseModel):
	ip: IPv4Address
	service_name: str

	class Config:
		schema_extra = {
			"example": {
				"ip": "192.168.1.18",
				"service_name": "RISAPI8142"
			}
		}


class ServiceOperation(BaseModel):
	ip: IPv4Address
	operation: str
	service_name: str

	class Config:
		schema_extra = {
			"example": {
				"ip": "192.168.1.18",
				"operation": "start",
				"service_name": "RISAPI8142"

			}
		}


if __name__ == "__main__":
	cci = CDClientIP(ip='192.168.3.6')
	print(str(cci.ip))
