"""
@File : business_auto_create_report.py
@Date : 2021/11/2 10:36
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""

# 根据测试单号自动生成报告
# import os
from fastapi import APIRouter
from app.models.test_task_model import TestTaskModel, get_build_details
from app.models.test_report_model import TestReportModel
from app.db.database import *
from app.models.bug_model import get_testtask_related_bug, get_testtask_bug_statistics, calculate_in_value, \
	evaluate_grade, release_evaluation
from app.schemas import test_report_schemas
from app.utils import response_code, html2string
from app.config import ROOT_DIRECTORY, AUTO_TEST_REPORT
from datetime import datetime
import os

REPORT_TEMPLATE_PATH = os.path.join(ROOT_DIRECTORY, 'static', AUTO_TEST_REPORT['TEMPLATE'])


# 生成报告总结
def report_summary(task_para: dict):
	summary_dict = dict()
	summary_dict['build'] = get_build_details(task_para['task_id']).get('name')  # 测试总结的标题使用
	if task_para['test_time']:
		summary_dict['testTime'] = task_para['test_time']
	else:
		summary_dict['testTime'] = '填写测试耗时.e.g. 1MD、0.5MD、3MH'
	if task_para['test_url']:
		summary_dict['testURL'] = task_para['test_url']
	else:
		summary_dict['testURL'] = '填写测试地址 e.g. http://test.ris.com'
	if task_para['test_client']:
		summary_dict['testClient'] = task_para['test_client']
	else:
		summary_dict['testClient'] = 'Win10Pro Core(TM) i5-7500 CPU 16G RAM、Chrome 版本 95.0.4638.69(根据实际情况填写客户机配置及浏览器版本)'
	if task_para['test_tool']:
		summary_dict['testTools'] = task_para['test_tool']
	else:
		summary_dict['testTools'] = 'DevTools'
	if task_para['test_content']:
		summary_dict['testTask'] = task_para['test_content']
	else:
		summary_dict['testTask'] = get_build_details(str(task_para['task_id'])).get('desc')
	if task_para['risk_evaluation']:
		summary_dict['riskEvaluation'] = task_para['risk_evaluation']
	else:
		summary_dict['riskEvaluation'] = "填写测试过程中未能规避的风险"
	if task_para['summary']:
		summary_dict['summary'] = task_para['summary']
	else:
		summary_dict['summary'] = "对本次版本测试的总结"
	in_value = calculate_in_value(get_testtask_bug_statistics(task_para['task_id']))
	summary_dict['instabilityValue'] = in_value
	summary_dict['quality'] = evaluate_grade(in_value)
	summary_dict['if_release'] = release_evaluation(in_value)
	return summary_dict


# def report_summary(task_id):
# 	summary_dict = dict()
# 	in_value = calculate_in_value(get_testtask_bug_statistics(task_id))
# 	summary_dict['build'] = get_build_details(task_id).get('name')  # 测试总结的标题使用
# 	summary_dict['testTime'] = '填写测试耗时.e.g. 1MD、0.5MD、3MH'
# 	summary_dict['testURL'] = '填写测试地址 e.g. http://test.ris.com'
# 	summary_dict['testClient'] = 'Win10Pro Core(TM) i5-7500 CPU 16G RAM、Chrome 版本 95.0.4638.69(根据实际情况填写客户机配置及浏览器版本)'
# 	summary_dict['testTools'] = 'DevTools'
# 	summary_dict['testTask'] = get_build_details(task_id).get('desc')
# 	summary_dict['riskEvaluation'] = "填写测试过程中未能规避的风险"
# 	summary_dict['summary'] = "对本次版本测试的总结"
# 	summary_dict['instabilityValue'] = in_value
# 	summary_dict['quality'] = evaluate_grade(in_value)
# 	summary_dict['if_release'] = release_evaluation(in_value)
# 	return summary_dict


# def generate_report(task_id):
# 	"""根据测试单的状态判断能否生成"""
# 	task = get(task_id, TestTaskModel).to_dict()
# 	if task.get('status') == 'done':
# 		report_dict = dict()
# 		report_dict['product'] = task['product']
# 		report_dict['project'] = task['project']
# 		report_dict['tasks'] = task_id
# 		report_dict['owner'] = task['owner']
# 		report_dict['begin'] = task['begin']
# 		report_dict['end'] = task['end']
# 		report_dict['members'] = task['mailto']
# 		report_dict['title'] = '{0} TESTTASK#{1} {2} 测试报告'.format(task['end'], task['id'], task['name'])
# 		report_dict['report'] = html2string.report_html2string(REPORT_TEMPLATE_PATH,
# 															   report_summary(task_id))
# 		report_dict['bugs'] = get_testtask_related_bug(task_id)
# 		report_dict['cases'] = ''
# 		report_dict['stories'] = ''
# 		report_dict['builds'] = task['build']
# 		report_dict['objectType'] = 'testtask'
# 		report_dict['objectID'] = task['id']
# 		report_dict['createdBy'] = task['owner']
# 	else:
# 		print('测试单{}未完成，不能生成测试报告'.format(task['id']))
# 		report_dict = dict()
# 	return report_dict

def generate_report(task_para: dict):
	"""根据测试单的状态判断能否生成"""
	task = get(task_para['task_id'], TestTaskModel).to_dict()
	report_dict = dict()
	report_dict['product'] = task['product']
	report_dict['project'] = task['project']
	report_dict['tasks'] = task_para['task_id']
	report_dict['owner'] = task['owner']
	report_dict['begin'] = task['begin']
	report_dict['end'] = task['end']
	report_dict['members'] = task['mailto']
	report_dict['title'] = '{0} TESTTASK#{1} {2} 测试报告'.format(task['end'], task['id'], task['name'])
	report_dict['report'] = html2string.report_html2string(REPORT_TEMPLATE_PATH,
														   report_summary(task_para))
	report_dict['bugs'] = get_testtask_related_bug(task_para['task_id'])
	report_dict['cases'] = ''
	report_dict['stories'] = ''
	report_dict['builds'] = task['build']
	report_dict['objectType'] = 'testtask'
	report_dict['objectID'] = task['id']
	report_dict['createdBy'] = task['owner']
	report_dict['createdDate'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

	return report_dict


router = APIRouter(prefix="/ewordci/auto-report", tags=["business"])


@router.post("/create", name="自动生成测试报告")
async def generate_test_report(task_para: test_report_schemas.AutoTestReport):
	report_dict = generate_report(task_para.dict())  # 通过测试单号获取报告需要的信息
	report_schemas = test_report_schemas.TestReport(**report_dict)  # 传字典schema实例化
	db_test_report = TestReportModel(report_schemas.dict())  # 实例化数据模型
	create(db_test_report)  # 调用create插入数据库
	if db_test_report.id:  # 根据有没有生成新的id判断是否插入成功
		return response_code.resp_200(db_test_report.to_dict(),
									  message='测试单{}的测试报告生成成功'.format(task_para.dict()['task_id']))
	else:
		return response_code.resp_400(message="生成报告失败")


@router.post("/create-in-batches", name="自动批量生成测试报告")
async def generate_report_in_batches(task_para_list: list[test_report_schemas.AutoTestReport]):
	db_test_report_list = list()
	for task_para in task_para_list:
		report_dict = generate_report(task_para.dict())
		report_schemas = test_report_schemas.TestReport(**report_dict)
		db_test_report_list.append(TestReportModel(report_schemas.dict()))
	create_all(db_test_report_list)
	task_id_list = [task.task_id for task in task_para_list]  # 提取请求的测试单id列表
	test_report_list = [test_report.to_dict() for test_report in db_test_report_list]  # 提取生成报告单的列表
	# 根据请求插入的记录的list长度比较，判断是否全部插入
	if len(test_report_list) == len(task_id_list):
		return response_code.resp_200(test_report_list, message='测试单{}的报告全部生成成功'.format(task_id_list))
	else:
		return response_code.resp_400(message='测试报告未能全部生成，成功的测试单有{}'.format(task_id_list))


if __name__ == "__main__":
	print(REPORT_TEMPLATE_PATH)
