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
def check_if_online(client_ip: str, client_port: int):
	try:
		res = get('http://{0}:{1}/ewordcd/check'.format(client_ip, client_port),
				  timeout=0.5)  # 加个超时时间，当超过500ms就认为链接客户端CD接口失败
		status_code = res.status_code
		if status_code == 200:
			custom_log.logging.info("检测{0}:{1}的状态为{2}".format(client_ip, client_port, status_code))
			return True
		else:
			custom_log.logging.info("检测{0}:{1}的状态为{2}".format(client_ip, client_port, status_code))
			return False
	except Exception as e:
		custom_log.logging.error(str(e))
		return False


router = APIRouter(prefix="/ewordci/cd_server", tags=["cd_server"])

"""业务类"""


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
		# 读取内容判断是否已经存在相同客户端ip+port,没有则追加
		elif (rg_para_dict['ip'], rg_para_dict['port']) not in [(item.get('ip'), item.get('port')) for item in
																CD_CLIENT_INFO]:
			CD_CLIENT_INFO.append(rg_para_dict)
			json_rw.write_json(CD_CLIENT_INFO)
			custom_log.logging.info("注册成功{}".format(rg_para_dict))
			return response_code.resp_200({}, message="注册成功{}".format(rg_para_dict))
		else:  # 存在相同的客户端ip+port,注册时将在线标记标记成true
			for item in CD_CLIENT_INFO:
				if (rg_para_dict['ip'], rg_para_dict['port']) == (item.get('ip'), item.get('port')):
					item['online'] = True
					# item['desc'] = rg_para_dict['desc']
					json_rw.write_json(CD_CLIENT_INFO)
					break
			custom_log.logging.info("相同客户端已注册，激活在线标记")
			return response_code.resp_200({}, message="相同客户端已注册，激活在线标记")
	except Exception as e:
		custom_log.logging.error(str(e))
		return response_code.resp_500(message=str(e))


# 获取CD注册信息
@router.get("/get-cd-clients", name="获取CD客户端列表信息")
async def get_cd_clients_info():
	try:
		if CD_CLIENT_INFO:
			for info in CD_CLIENT_INFO:
				info['online'] = check_if_online(info['ip'], info['port'])
		json_rw.write_json(CD_CLIENT_INFO)  # 检测后更新注册信息
		return response_code.resp_200(CD_CLIENT_INFO)
	except Exception as e:
		custom_log.logging.error(str(e))
		return response_code.resp_500(message=str(e))


# 修改注册信息
@router.post("/update-cd-clients", name="修改注册信息")
async def update_cd_clients_info(client_infos: list[dict]):
	global CD_CLIENT_INFO
	try:
		json_rw.write_json(client_infos)
		CD_CLIENT_INFO = client_infos
		custom_log.logging.info("修改注册信息成功{}".format(CD_CLIENT_INFO))
		return response_code.resp_200(CD_CLIENT_INFO, message="修改注册信息成功")
	except Exception as e:
		custom_log.logging.error(str(e))
		return response_code.resp_500(message=str(e))


# 查看服务器是否被远程
@router.post("/cd-client-if-remoted", name="查看服务器是否被远程")
async def check_client_remoted(client: CD_schemas.CDClient):
	res = get(url=f"http://{client.ip}:{client.port}/ewordcd/tools/if_remoted",timeout=2)
	if res.json()['code'] == 200:
		return response_code.resp_200(res.json()['data'], message=res.json()['message'])
	else:
		return response_code.resp_500(res.json()['message'])


# 部署程序
@router.post("/application/deploy", name="部署程序")
async def application_deploy(app_deploy: CD_schemas.AppDeploy):
	if CD_CLIENT_INFO:
		# 判断对应的服务器上是否注册和安装了CD客户端
		check_li = [(client['ip'], client['online']) for client in CD_CLIENT_INFO]
		if (str(app_deploy.cd_client.ip), True) in check_li:
			try:
				res = post(url='http://{0}:{1}/ewordcd/application/deploy'.format(app_deploy.cd_client.ip,
																				  app_deploy.cd_client.port),
						   json=app_deploy.deploy_para.dict())
				if res.json()['code'] == 200:
					return response_code.resp_200({}, message=res.json()['message'])
				else:
					return response_code.resp_500(res.json()['message'])
			except Exception as e:
				return response_code.resp_500(str(e))
		else:
			return response_code.resp_204(message="该CD客户端未注册或已离线")
	else:
		return response_code.resp_204(message="无注册的CD客户端")


# 更新程序
@router.post("/application/upgrade", name="更新程序")
def application_upgrade(upgrade_para: CD_schemas.AppUpgrade):
	if CD_CLIENT_INFO:
		# 判断对应的服务器上是否注册和安装了CD客户端
		check_li = [(client['ip'], client['online']) for client in CD_CLIENT_INFO]
		if (str(upgrade_para.cd_client.ip), True) in check_li:
			res = post(
				url=f"http://{upgrade_para.cd_client.ip}:{upgrade_para.cd_client.port}/ewordcd/application/upgrade",
				json=upgrade_para.app_para.dict())
			if res.status_code == 200:
				return response_code.resp_200({}, message="更新成功")
			else:
				error_message = res.json()['message']
				custom_log.logging.error(f"{error_message}")
				return response_code.resp_400(error_message)
		else:
			return response_code.resp_204(message="该CD客户端未注册或已离线")
	else:
		return response_code.resp_204(message="无注册的CD客户端")


"""工具类"""


# 获取tomtaw服务列表
@router.post("/find_tomtaw_services", name="查找公司的服务信息")
# TODO 验证一下卡死问题，卡死步骤：切到服务列表，启动相应的CD服务，然后停止CD服务查看，19CI服务情况
# async def find_tomtaw_services(client_info: CD_schemas.CDClient):
def find_tomtaw_services(client_info: CD_schemas.CDClient):  # 防止服务卡死，不使用aysnc
	try:
		res = get(url='http://{0}:{1}/ewordcd/tools/find_tomtaw_services'.format(client_info.ip, client_info.port),
				  params=None)
		if res.json()['code'] == 200:
			return response_code.resp_200(res.json()['data'])
		else:
			return response_code.resp_204()
	except Exception as e:
		return response_code.resp_500(str(e))


# 根据服务名获取服务信息
@router.post("/get_service_info", name="根据服务名获取服务信息")
async def get_service_info(service_query: CD_schemas.ServiceQuery):
	try:
		res = get(url='http://{0}:{1}/ewordcd/tools/get_service_info'.format(service_query.cd_client.ip,
																			 service_query.cd_client.port),
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
		res = post(url='http://{0}:{1}/ewordcd/tools/service_operation'.format(operation_param.cd_client.ip,
																			   operation_param.cd_client.port),
				   json={'operation': operation_param.operation, 'service_name': operation_param.service_name})
		if res.json():
			return response_code.resp_200(res.json()['data'])
		else:
			return response_code.resp_204()
	except Exception as e:
		return response_code.resp_500(str(e))


# 找查找配置文件
@router.post("/find_config_files", name="查找配置文件(程序所需的json\config等配置文件，匹配目标固定)")
async def find_configs(config_param: CD_schemas.ConfigFiles):
	try:
		res = get(
			url=f'http://{config_param.cd_client.ip}:{config_param.cd_client.port}/ewordcd/tools/find_config_files',
			params={"directory": config_param.directory})
		if res.json():
			return response_code.resp_200(res.json()['data'])
		else:
			return response_code.resp_204()
	except Exception as e:
		return response_code.resp_500(str(e))


# 根据入参匹配遍历文件
@router.post("/find_config_files_with_match", name="根据入参匹配查找配置文件")
async def find_configs_with_param(config_param: CD_schemas.ConfigFilesWithParam):
	try:
		res = post(url='http://{0}:{1}/ewordcd/tools/find_config_files_with_match'.format(config_param.cd_client.ip,
																						  config_param.cd_client.port),
				   json={'directory': config_param.directory, 'file_name': config_param.file_name,
						 'file_suffix': config_param.file_suffix})
		if res.json():
			return response_code.resp_200(res.json()['data'])
		else:
			return response_code.resp_204()
	except Exception as e:
		return response_code.resp_500(str(e))


# 读取文件
@router.post("/read_file", name="读取文件内容")
async def read_file_content(read_para: CD_schemas.ReadConfig):
	try:
		res = post(
			url='http://{0}:{1}/ewordcd/tools/read_file'.format(read_para.cd_client.ip, read_para.cd_client.port),
			json={'config_path': read_para.config_path})
		if res.json():
			return response_code.resp_200(res.json()['data'], "读取文件成功")
		else:
			return response_code.resp_204()
	except Exception as e:
		return response_code.resp_500(message="读取文件失败，原因{}".format(str(e)))


# 修改文件
@router.post("/write_file", name="写入文件内容")
async def write_file_content(write_para: CD_schemas.WriteConfig):
	try:
		res = post(
			url='http://{0}:{1}/ewordcd/tools/write_file'.format(write_para.cd_client.ip, write_para.cd_client.port),
			json={'config_path': write_para.config_path, 'write_content': write_para.write_content})
		if res.json():
			return response_code.resp_200({}, message="写入成功")
		else:
			return response_code.resp_204()
	except Exception as e:
		return response_code.resp_500(message="写入失败，原因{}".format(str(e)))


# 端口号检测
@router.post("/check_port", name="检测端口号是否可用")
async def check_port_if_available(port_para: CD_schemas.CheckPort):
	try:
		res = get(
			url='http://{0}:{1}/ewordcd/tools/check_port'.format(port_para.cd_client.ip, port_para.cd_client.port),
			params={'port': port_para.port})
		if res.json()['data']:
			return response_code.resp_200(res.json()['data'], res.json()['message'])
		else:
			return response_code.resp_204(res.json()['data'], res.json()['message'])
	except Exception as e:
		return response_code.resp_500(message="检测端口号失败，原因{}".format(str(e)))


if __name__ == "__main__":
	# print(CD_CLIENT_INFO)
	# check_if_online('192.168.1.56', 8888)
	pass
