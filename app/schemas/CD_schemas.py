"""
@File : CD_schemas.py
@Date : 2022/1/24 15:50
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""
from pydantic import BaseModel
from typing import Optional, Text
from ipaddress import IPv4Address


class CDRegister(BaseModel):
	hostname: str
	ip: IPv4Address
	port: int
	desc: Optional[str]
	online: bool

	class Config:
		schema_extra = {
			"example": {
				"hostname": 'DESKTOP-L7R9KAB',
				"ip": "192.168.1.56",
				"port": 8888,
				"desc": "测试机",
				"online": True
			}
		}


"""服务更新参数"""


class AppParameter(BaseModel):
	task_id: int
	service_name: str
	config_files: list[list]

	class Config:
		schema_extra = {
			"example": {
				"task_id": 726,
				"service_name": 'eWordRISAPI',
				"config_files": [[
					r"E:\eWord\RIS\WebSite",
					"appsettings.json"
				],
					[
						r"E:\eWord\RIS\WebSite",
						"DBConfig.json"
					],
					[
						r"E:\eWord\RIS\WebSite",
						"log4net.config"
					]]
			}
		}


class CDClient(BaseModel):
	ip: IPv4Address
	port: int

	class Config:
		schema_extra = {
			"example": {
				"ip": "192.168.1.18",
				"port": 8888
			}
		}


class AppUpgrade(BaseModel):
	cd_client: CDClient
	app_para: AppParameter


"""服务部署的参数"""


class DeployPara(BaseModel):
	deploy_path: str
	deploy_folder: Optional[str]
	file_path: Optional[str]
	build_id: Optional[int]
	service_name: Optional[str]


class AppDeploy(BaseModel):
	cd_client: CDClient
	deploy_para: DeployPara

	class Config:
		schema_extra = {
			"example": {
				"cd_client":
					{
						"ip": "192.168.1.18",
						"port": 8887
					}
				, "deploy_para": {
					"deploy_path": r"D:\eWord\RIS",
					"deploy_folder": r"WebSite（可选，不传则以拉取的文件夹名为准）",
					"file_path": r"\\192.168.1.19\delivery\eWordRIS\V2.2.0.4286.20211117（可选，与build_id,二选一）",
					"build_id": 715,
					"service_name": "eWordRIS(可选，不传则以exe的文件名为准)"
				}

			}
		}


# 读取配置文件参数
class ReadConfig(BaseModel):
	cd_client: CDClient
	config_path: str


# 写入的内容
class WriteConfig(ReadConfig):
	write_content: Text


"""服务操作参数"""


class ServiceQuery(BaseModel):
	# ip: IPv4Address
	cd_client: CDClient
	service_name: str

	class Config:
		schema_extra = {
			"example": {
				# "ip": "192.168.1.18",
				"cd_client": {
					"ip": "192.168.1.18",
					"service_name": "RISAPI8142"
				},
				"service_name": "RISAPI8142"
			}
		}


class ServiceOperation(BaseModel):
	# ip: IPv4Address
	cd_client: CDClient
	operation: str
	service_name: str

	class Config:
		schema_extra = {
			"example": {
				# "ip": "192.168.1.18",
				"cd_client": {
					"ip": "192.168.1.18",
					"port": 8887
				},
				"operation": "start",
				"service_name": "RISAPI8142"
			}
		}


class ConfigFiles(BaseModel):
	cd_client: CDClient
	directory: str

	class Config:
		schema_extra = {
			"example": {
				"cd_client": {
					"ip": "192.168.1.18",
					"port": 8887
				},
				"directory": r"D:\producttest\eWordRIS\WebSite"
			}
		}


if __name__ == "__main__":
	cci = CDClient(ip='192.168.3.6')
	print(str(cci.ip))
