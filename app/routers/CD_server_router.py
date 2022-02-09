"""
@File : CD_server_router.py
@Date : 2022/1/24 14:34
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""
from fastapi import APIRouter
from app.schemas import CD_schemas
from app.utils import response_code, json_rw, custom_log
from requests import get, post

CD_CLIENT_INFO = json_rw.read_json()


# 检测CD客户端是否在线
def check_if_online(url):
	try:
		res = get('http://{}:8888/ewordcd/check'.format(url), timeout=0.5)  # 加个超时时间，当超过500ms就认为链接客户端CD接口失败
		status_code = res.status_code
		if status_code == 200:
			custom_log.logging.info("检测{0}:8888的状态为{1}".format(url, status_code))
			return True
		else:
			custom_log.logging.info("检测{0}:8888的状态为{1}".format(url, status_code))
			return False
	except Exception as e:
		custom_log.logging.error(str(e))
		return False


router = APIRouter(prefix="/ewordci/cd_server", tags=["cd_server"])


# CD注册接口
@router.post("/register", name="注册CD客户端")
async def register(rg_para: CD_schemas.CDRegister):
	global CD_CLIENT_INFO
	rg_para_dict = rg_para.dict()
	rg_para_dict['ip'] = str(rg_para_dict['ip'])  # ip的对象转化字符串
	try:
		# 判断配置文件是否有内容
		if not CD_CLIENT_INFO:
			CD_CLIENT_INFO = [rg_para_dict]
			json_rw.write_json(CD_CLIENT_INFO)
			custom_log.logging.info("注册成功{}".format(CD_CLIENT_INFO))
			return response_code.resp_200({}, message="注册成功{}".format(rg_para_dict))
		# 读取内容判断是否已经存在相同客户端ip
		elif rg_para_dict['ip'] not in [item.get('ip') for item in CD_CLIENT_INFO]:
			CD_CLIENT_INFO.append(rg_para_dict)
			json_rw.write_json(CD_CLIENT_INFO)
			custom_log.logging.info("注册成功{}".format(rg_para_dict))
			return response_code.resp_200({}, message="注册成功{}".format(rg_para_dict))
		else:
			custom_log.logging.info("已存在相同ip的客户端")
			return response_code.resp_204(message="已存在相同ip的客户端")
	except Exception as e:
		custom_log.logging.error(str(e))
		return response_code.resp_500(message=str(e))


# 获取CD注册信息
@router.get("/get-cd-clients", name="获取CD客户端列表信息")
async def get_cd_clients_info():
	try:
		if CD_CLIENT_INFO:
			for info in CD_CLIENT_INFO:
				info['online'] = check_if_online(info['ip'])
		return response_code.resp_200(CD_CLIENT_INFO)
	except Exception as e:
		custom_log.logging.error(str(e))
		return response_code.resp_500(message=str(e))


# 修改注册信息
@router.post("/update-cd-clients", name="修改注册信息")
async def get_cd_clients_info(client_infos: list[dict]):
	global CD_CLIENT_INFO
	try:
		json_rw.write_json(client_infos)
		CD_CLIENT_INFO = client_infos
		custom_log.logging.info("修改注册信息成功{}".format(CD_CLIENT_INFO))
		return response_code.resp_200(CD_CLIENT_INFO, message="修改注册信息成功")
	except Exception as e:
		custom_log.logging.error(str(e))
		return response_code.resp_500(message=str(e))


# 更新程序
@router.post("/application/upgrade", name="更新程序")
async def application_upgrade(upgrade_para: CD_schemas.AppUpgrade):
	if CD_CLIENT_INFO:
		# 判断对应的服务器上是否注册和安装了CD客户端
		check_li = [(client['ip'], client['online']) for client in CD_CLIENT_INFO]
		if (upgrade_para.CD_url, True) in check_li:
			try:
				post(url='http://{0}:8888/ewordcd/application/upgrade'.format(upgrade_para.CD_url),
					 json=upgrade_para.app_para.dict())
				return response_code.resp_200({})
			except Exception as e:
				return response_code.resp_500(str(e))
		else:
			return response_code.resp_204(message="该CD客户端未注册或已离线")
	else:
		return response_code.resp_204(message="无注册的CD客户端")


# 获取tomtaw服务列表
@router.post("/find_tomtaw_services", name="查找公司的服务信息")
async def find_tomtaw_services(ip_address: CD_schemas.CDClientIP):
	try:
		res = get(url='http://{0}:8888/ewordcd/tools/find_tomtaw_services'.format(ip_address.ip), params=None)
		if res.json():
			return response_code.resp_200(res.json()['data'])
		else:
			return response_code.resp_204()
	except Exception as e:
		return response_code.resp_500(str(e))


# 根据服务名获取服务信息
@router.post("/get_service_info", name="根据服务名获取服务信息")
async def get_service_info(service_query: CD_schemas.ServiceQuery):
	try:
		res = get(url='http://{0}:8888/ewordcd/tools/get_service_info'.format(service_query.ip),
				  params={'service_name': service_query.service_name})
		if res.json():
			return response_code.resp_200(res.json()['data'])
		else:
			return response_code.resp_204()
	except Exception as e:
		return response_code.resp_500(str(e))


# 服务操作
@router.post("/service_operation", name="服务操作")
async def service_operation(operation_param: CD_schemas.ServiceOperation):
	try:
		res = post(url='http://{0}:8888/ewordcd/tools/service_operation'.format(operation_param.ip),
				   json={'operation': operation_param.operation, 'service_name': operation_param.service_name})
		if res.json():
			return response_code.resp_200(res.json()['data'])
		else:
			return response_code.resp_204()
	except Exception as e:
		return response_code.resp_500(str(e))


# 安装程序

if __name__ == "__main__":
	# print(CD_CLIENT_INFO)
	check_if_online('192.168.1.56')
