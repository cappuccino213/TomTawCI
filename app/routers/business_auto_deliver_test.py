"""
@File : business_auto_deliver_test.py
@Date : 2021/11/24 9:15
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""
from fastapi import APIRouter
from app.schemas import test_deliver_schemas, build_schemas, test_task_schemas
from app.utils import response_code, html2string
from app.models.build_model import *
from app.db.database import *
from app.models.test_task_model import *
from app.models.action_model import *
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
	# print(query_condition)
	build_list = query_build_multiple_condition(query_condition)
	build_id = build_list[0].id
	# 获取测试单参数
	task_name = "{}{}{} 测试申请".format(parameter.project_name, parameter.new_build_name,
									 parameter.test_type)
	test_desc_dict = dict(ifSmoke=parameter.if_smoke,
						  manTime=parameter.man_time,
						  testType=parameter.test_type,
						  testSuggest=parameter.test_suggest,
						  buildDesc=parameter.desc)
	task_desc = html2string.task_html2string(TEST_TASK_TEMPLATE_PATH, test_desc_dict)
	test_task_dict = dict(name=task_name, product=parameter.product_id, project=parameter.project_id, build=build_id,
						  owner=parameter.owner, pri=parameter.pri, mailto=parameter.mailto, desc=task_desc,
						  begin=parameter.begin,
						  end=parameter.end)
	return test_task_dict


@router.post("/create", name="自动创建版本、创建测试单")
async def generate_deliver_task(deliver_info: test_deliver_schemas.Deliver):
	# 新建、修改版本处理
	if deliver_info.old_build_id:  # 通过是入参中是否传老版本id判断是修改还是新增
		# 获取入参的版本信息
		update_build_schema = para_deliver2build_schema(deliver_info)
		update_build_schema.name = deliver_info.new_build_name
		update_build_schema.desc = deliver_info.desc
		update_build_schema.scmPath = deliver_info.scmPath
		update_build_schema.filePath = deliver_info.filePath
		update(update_build_schema, BuildModel)
		# 插入操作日志
		db_action = ActionModel(
			get_action_dict('build', deliver_info.old_build_id, deliver_info.product_id, deliver_info.project_id,
							deliver_info.builder, 'edited'))
		create(db_action)
		build_handle_flag = True
		build_handle_message = "版本修改成功"
	else:
		# 判断新增的数据版本号是否重复
		condition = dict(name=deliver_info.new_build_name, product=deliver_info.product_id,
						 project=deliver_info.project_id)  # 版本查询条件
		if query_build_multiple_condition(condition):
			build_handle_flag = False
			build_handle_message = "已存在同的版本"
		else:
			create_build_schema = para_deliver2build_schema(deliver_info)
			db_build = BuildModel(create_build_schema.dict())
			create(db_build)
			# 插入操作日志
			db_action = ActionModel(
				get_action_dict('build', db_build.id, deliver_info.product_id, deliver_info.project_id,
								deliver_info.builder, 'opened'))
			create(db_action)
			build_handle_flag = True
			build_handle_message = "版本创建成功"
	task_handle_flag = False
	task_handle_message = ''
	success_task_id = 0  # 用于存放创建成功的测试单id
	if build_handle_flag:  # 判断版本是否创建成功
		task_dict = para_deliver2task(deliver_info)
		# 判断此版本号的测试单是否存在，若存在则修改，不存在则创建
		# 根据版本号查询测试单
		update_test_task = query_testtask(dict(build=task_dict['build']))
		if update_test_task:
			update_task_schema = test_task_schemas.TestTask(**task_dict)
			update_task_schema.id = update_test_task.id
			update(update_task_schema, TestTaskModel)
			# 插入操作日志
			db_action = ActionModel(
				get_action_dict('testtask', update_task_schema.id, deliver_info.product_id, deliver_info.project_id,
								deliver_info.builder, 'edited'))
			create(db_action)
			task_handle_message = "测试单修改成功"
			success_task_id = update_test_task.id
		else:
			db_test_task = TestTaskModel(task_dict)
			create(db_test_task)
			# 插入操作日志
			db_action = ActionModel(
				get_action_dict('testtask', db_test_task.id,deliver_info.product_id, deliver_info.project_id,
								deliver_info.builder, 'opened'))
			create(db_action)
			task_handle_message = "测试单创建成功"
			success_task_id = db_test_task.id
		task_handle_flag = True
	if build_handle_flag and task_handle_flag:
		return response_code.resp_200(success_task_id,
									  message='{}且{}'.format(build_handle_message, task_handle_message))
	else:
		return response_code.resp_204(message=build_handle_message)


if __name__ == "__main__":
	pass
