"""
@File : CI_server_router.py
@Date : 2022/3/30 15:03
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder

from app.utils import response_code
from app.utils import multiple_thread

from app.schemas.CI_schemas import *

from app.models.ci_server_model import *

from app.db.database import *

import subprocess

router = APIRouter(prefix="/ewordci/ci_server", tags=["ci_server"])


# 检测API是否启动
@router.get("/check", name="检测API服务是否正常启动")
# async def check():
def check():  # 防止接口耗时到时请求堵塞，使用同步
	return response_code.resp_200("WelCome to eWordCI", message="Success")


"""ServerMonitor"""


# 检查服务器是否能ping通
def check_server_online(host):
	result = subprocess.Popen(f"ping {host} -n 1", stdout=subprocess.PIPE, universal_newlines=True, shell=True)
	stdout, stderr = result.communicate()
	# print(type(stdout))
	if "无法访问" in stdout:
		return {'ip': host, 'status': False}
	else:
		return {'ip': host, 'status': True}


@router.post("/server_monitor", name="检测服务器是否在线")
# async def server_monitor(param: ServerCheck):
# 	if param.ip_list:
# 		result = [check_server_online(ip_add) for ip_add in param.ip_list]
# 		return response_code.resp_200(result)
# 	else:
# 		return response_code.resp_400(message="参数不能为空")
# 使用多线程检测，加快响应速度 #当列表中的入参ip是一样的时候会不准
def server_monitor(param: ServerCheck):
	if param.ip_list:
		threads = []
		result = []
		for ip_add in param.ip_list:
			thread = multiple_thread.MultipleThread(check_server_online, args=(ip_add,))
			thread.start()
			threads.append(thread)
		for thread in threads:
			thread.join()
			result.append(thread.get_result())
		return response_code.resp_200(result)
	else:
		return response_code.resp_400(message="参数不能为空")


"""server的CRUD"""
Base.metadata.create_all(bind=engine)


# add
@router.post("/add", response_model=Server, name="增加服务器")
async def add_server(param: AddServer):
	server_json = jsonable_encoder(param)
	db_server = ServerModel(server_json)
	# 先判断是否存在相同的ip记录
	try:
		if not if_ip_exist(param.ipAddress, ServerModel):
			create(db_server)
			if db_server.id:
				return response_code.resp_200(db_server.to_dict())
			else:
				return response_code.resp_400(message="新增服务器失败")
		else:
			return response_code.resp_400(message=f"ip为{param.ipAddress}的服务器已存在")
	except Exception as e:
		return response_code.resp_400(message=f"增加失败，异常str{e}")


# update
@router.put("/update", response_model=Server, name="修改服务器信息")
async def update_sever(param: Server):
	if_success = update(param, ServerModel)
	if if_success:
		return response_code.resp_200(param.dict(), message="修改服务器信息成功")
	else:
		return response_code.resp_404(message=f"修改id={param.id}的服务器信息失败")


# delete
@router.delete("/delete", name="删除服务器")
async def delete_sever(server_id: int):
	# 先判断是否存在相同的ip记录
	if_success = remove(server_id, ServerModel)
	if if_success:
		return response_code.resp_200([], message="删除服务器成功")
	else:
		return response_code.resp_404(message=f"删除id={server_id}的服务器失败")


# get
@router.get("/get", name="获取服务器信息")
async def get_server(server_id: int):
	db_server = get(server_id, ServerModel)
	if db_server:
		return response_code.resp_200(db_server.to_dict())
	else:
		return response_code.resp_404(message=f"找不到id={server_id}的服务器信息")


@router.get("/get_list", name="获取服务器信息列表")
async def get_servers():
	db_server = get_server_list(ServerModel)
	if db_server:
		return response_code.resp_200(db_server)
	else:
		return response_code.resp_404(message="查无记录")


if __name__ == "__main__":
	pass
	print(check_server_online('192.168.1.181'))
