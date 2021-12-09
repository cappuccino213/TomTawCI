"""
@File : business_auto_deliver_test.py
@Date : 2021/11/24 9:15
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""
from fastapi import APIRouter
from app.schemas import test_deliver_schemas, build_schemas
from app.utils import response_code, html2string
from app.models.build_model import *
from app.db.database import *
from datetime import date
from app.models.test_task_model import TestTaskModel
from app.config import ROOT_DIRECTORY, APPLY_TEST
import os

# TEST_TASK_TEMPLATE_PATH = r'D:\Python\Project\pythonProject\TomTawCI\app\static\testTaskDesc.html'
TEST_TASK_TEMPLATE_PATH = os.path.join(ROOT_DIRECTORY, 'static', APPLY_TEST['TEMPLATE'])

router = APIRouter(prefix="/ewordci/auto-deliver-test", tags=["business"])


# 处理deliver入参


def para_deliver2build_schema(parameter: test_deliver_schemas.Deliver):
	"""
	将入参解析处理成build的参数
	根据是否有传老版本id，来返回带有id的更新参数或者不带id的新增参数
	:param parameter:
	:return:build_schema
	"""
	build_schema = build_schemas.Build(name=parameter.new_build_name,
									   product=parameter.product_id,
									   project=parameter.project_id,
									   filePath=parameter.filePath,
									   scmPath=parameter.scmPath,
									   builder=parameter.builder,
									   desc=parameter.desc,
									   date=date.today())
	if parameter.old_build_id:  # 有旧版本id则为更新操作，需要将id加进去
		build_schema.id = parameter.old_build_id
	return build_schema


def para_deliver2task(parameter: test_deliver_schemas.Deliver):
	"""
	:param parameter:
	:return: 创建测试单需要的dict数据
	"""
	# 通过版本信息获取版本id，为了与测试单相关联
	query_condition = dict(product=parameter.product_id, project=parameter.project_id, name=parameter.new_build_name)

	build_id = query_multiple_condition(query_condition)[0].id  # TODO 当传入错误的版本号时，这里会有下标越界，需要处理一下

	# 获取测试单参数
	task_name = "{}{}{}{} 测试申请".format(parameter.product_name, parameter.project_name, parameter.new_build_name,
									   parameter.test_type)
	test_desc_dict = dict(ifSmoke=parameter.if_smoke,
						  manTime=parameter.man_time,
						  testType=parameter.test_type,
						  testSuggest=parameter.test_suggest,
						  buildDesc=parameter.desc)
	task_desc = html2string.task_html2string(TEST_TASK_TEMPLATE_PATH, test_desc_dict)
	test_task_dict = dict(name=task_name, product=parameter.product_id, project=parameter.project_id, build=build_id,
						  owner=parameter.owner, mailto=parameter.mailto, desc=task_desc, begin=parameter.begin,
						  end=parameter.end)
	return test_task_dict


# @router.post("/create1", name="自动创建版本、创建测试单")
# async def generate_deliver_task1(deliver_info: test_deliver_schemas.Deliver):
# 	# build_dict = para_deliver2build(deliver_info)
# 	# 判断同一个产品、项目下是否存在相同的版本号
# 	# condition = dict(name=build_dict['name'], product=build_dict['product'], project=build_dict['project'])
# 	condition = dict(name=deliver_info.new_build_name, product=deliver_info.product_id, project=deliver_info.project_id)
# 	if not query_multiple_condition(condition):
# 		build_dict = para_deliver2build(deliver_info)
# 		build_schema = build_schemas.Build(**build_dict)  # schema通过字典传入
# 		if build_dict.get('id') == 0:
# 			db_build = BuildModel(build_schema.dict())
# 			create(db_build)
# 			build_handle_flag = True
# 		else:
# 			update(build_schema, BuildModel)
# 			build_handle_flag = True
# 		# 处理测试单信息
# 		# assert build_handle_flag  # 当版本信息处理成功时才会继续处理测试单
# 		if build_handle_flag:  # 当版本信息处理成功时才会继续处理测试单
# 			task_dict = para_deliver2task(deliver_info)
# 			db_test_task = TestTaskModel(task_dict)
# 			create(db_test_task)
# 			return response_code.resp_200(dict(),
# 										  message='版本【{}】、测试单【{}】创建成功了呢'.format(build_dict.get('name'),
# 																				task_dict.get('name')))
# 	else:  # 存在相同版本号名称则不予创建
# 		return response_code.resp_204(message="同一个的产品及项目已存在此版本号")

@router.post("/create", name="自动创建版本、创建测试单")
async def generate_deliver_task(deliver_info: test_deliver_schemas.Deliver):
	# 新建、修改版本处理
	if deliver_info.old_build_id:  # 通过是入参中是否传老版本id判断是修改还是新增
		# 获取入参的版本信息
		update_build_schema = para_deliver2build_schema(deliver_info)
		update(update_build_schema, BuildModel)
		build_handle_flag = True
		build_handle_message = "版本修改成功"
	else:
		# 判断新增的数据版本号是否重复
		condition = dict(name=deliver_info.new_build_name, product=deliver_info.product_id,
						 project=deliver_info.project_id)  # 版本查询条件
		if query_multiple_condition(condition):
			build_handle_flag = False
			build_handle_message = "已存在同的版本"
		else:
			create_build_schema = para_deliver2build_schema(deliver_info)
			db_build = BuildModel(create_build_schema.dict())
			create(db_build)
			build_handle_flag = True
			build_handle_message = "版本创建成功"
	task_handle_flag = False
	task_handle_message = ''
	if build_handle_flag:
		task_dict = para_deliver2task(deliver_info)
		db_test_task = TestTaskModel(task_dict)
		create(db_test_task)
		task_handle_flag = True
		task_handle_message = "测试单创建成功"

	if build_handle_flag and task_handle_flag:
		return response_code.resp_200({},
									  message='{}且{}'.format(build_handle_message, task_handle_message))  # TODO 返回测试单信息
	else:
		return response_code.resp_204(message=build_handle_message)


if __name__ == "__main__":
	pass
