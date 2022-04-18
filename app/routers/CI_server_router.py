"""
@File : CI_server_router.py
@Date : 2022/3/30 15:03
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""
from fastapi import APIRouter

from app.utils import response_code

from schemas.CI_schemas import *

import subprocess

router = APIRouter(prefix="/ewordci/ci_server", tags=["ci_server"])


# 检测API是否启动
@router.get("/check", name="检测API服务是否正常启动")
async def check():
	return response_code.resp_200("WelCome to eWordCI", message="Success")


"""ServerMonitor"""


# 检查服务器是否能ping通
def check_server_online(host):
	result = subprocess.Popen(f"ping {host} -n 1", stdout=subprocess.PIPE, universal_newlines=True, shell=True)
	stdout, stderr = result.communicate()
	# print(type(stdout))
	if "无法访问" in stdout:
		return host, False
	else:
		return host, True


@router.post("/server_monitor", name="检测服务器是否在线")
async def server_monitor(param: ServerCheck):
	if param.ip_list:
		result = [check_server_online(ip_add) for ip_add in param.ip_list]
		return response_code.resp_200(result)
	else:
		return response_code.resp_400(message="参数不能为空")


if __name__ == "__main__":
	pass
	print(check_server_online('192.168.1.181'))
