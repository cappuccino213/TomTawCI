"""
@File : business_auto_deliver_test.py
@Date : 2021/11/24 9:15
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""
from fastapi import APIRouter
from app.schemas import test_deliver_shemas, build_schemas
from app.utils import response_code, html2string
from app.db.database import *
from app.models.build_model import *
from app.models.test_task_model import TestTaskModel

TEST_TASK_TEMPLATE_PATH = r'D:\Python\Project\pythonProject\TomTawCI\app\static\testTaskDesc.html'

router = APIRouter(prefix="/ewordci/auto-deliver-test", tags=["auto-business"])


# 处理deliver入参
def para_deliver2build(parameter: test_deliver_shemas.Deliver):
	"""
	将入参解析处理分成build的参数
	:param parameter:
	:return:
	"""
	deliver_dict = parameter.dict()
	build_dict = dict(id=deliver_dict['old_build_id'], name=deliver_dict['new_build_name'],
					  product=deliver_dict['product_id'],
					  project=deliver_dict['project_id'], scmPath=deliver_dict['scmPath'],
					  filePath=deliver_dict['filePath'],
					  builder=deliver_dict['builder'], desc=deliver_dict['desc'])

	return build_dict


def para_deliver2task(parameter: test_deliver_shemas.Deliver):
	deliver_dict = parameter.dict()
	build_condition = dict(product=deliver_dict['product_id'], project=deliver_dict['project_id'],
						   name=deliver_dict['new_build_name'])

	build_info = query_multiple_condition(build_condition)[0].to_dict()  # 从入参的产品、项目、版本名获取版本信息

	# 获取测试单参数
	task_name = "{}{}{}{} 测试申请".format(deliver_dict['product_name'], deliver_dict['project_name'],
									   deliver_dict['new_build_name'], deliver_dict['test_type'])
	desc_dict = dict(ifSmoke=deliver_dict['if_smoke'], manTime=deliver_dict['man_time'],
					 testType=deliver_dict['test_type'], testSuggest=deliver_dict['test_suggest'])
	task_desc = html2string.task_html2string(TEST_TASK_TEMPLATE_PATH, desc_dict)

	test_task_dict = dict(name=task_name, product=deliver_dict['product_id'], project=deliver_dict['project_id'],
						  build=build_info['id'], owner=deliver_dict['owner'], mailto=deliver_dict['mailto'],
						  desc=task_desc)

	return test_task_dict


@router.post("/create", name="自动创建版本、创建测试单")
async def generate_deliver_task(deliver_info: test_deliver_shemas.Deliver):
	build_dict = para_deliver2build(deliver_info)
	# 判断同一个产品、项目下是否存在相同的版本号
	condition = dict(name=build_dict['name'], product=build_dict['product'], project=build_dict['project'])
	if not query_multiple_condition(condition):
		build_schema = build_schemas.Build(**build_dict)  # schema通过字典传入
		if build_dict.get('id') == 0:
			db_build = BuildModel(build_schema.dict())
			create(db_build)
			build_handle_flag = True
		else:
			update(build_schema, BuildModel)
			build_handle_flag = True
		# 处理测试单信息
		assert build_handle_flag  # 当版本信息处理成功时才会继续处理测试单
		if build_handle_flag:  # 当版本信息处理成功时才会继续处理测试单
			task_dict = para_deliver2task(deliver_info)
			db_test_task = TestTaskModel(task_dict)
			create(db_test_task)
			return response_code.resp_200(dict(),
										  message='版本【{}】、测试单【{}】创建成功了呢'.format(build_dict.get('name'),
																				task_dict.get('name')))
	else:  # 存在相同版本号名称则不予创建
		return response_code.resp_200(dict(), message="同一个的产品及项目已存在此版本号")


if __name__ == "__main__":
	pass
# d = {
# 	"product_id": 7,
# 	"product_name": "产品名称",
# 	"project_id": 66,
# 	"project_name": "项目名称",
# 	"if_smoke": "是",
# 	"man_time": "1MD",
# 	"old_build_id": 0,
# 	"new_build_name": "v1.0.0.3",
# 	"builder": "wangj",
# 	"desc": "版本信息描述",
# 	"scmPath": "\\\\192.168.1.19\\delivery\\eWordRIS\\V2.2.0.4286.20211117（源码路径，可选）",
# 	"filePath": "\\\\192.168.1.19\\delivery\\eWordRIS\\V2.2.0.4286.20211117（文件路径，可选）",
# 	"owner": "zyp",
# 	"mailto": ",zyp,zhangl",
# 	"test_type": "接口",
# 	"test_suggest": "测试建议"
# }
# deliver_info = test_deliver_shemas.Deliver(**d)
# build_dict = para_deliver2build(deliver_info)
# print(build_dict)
