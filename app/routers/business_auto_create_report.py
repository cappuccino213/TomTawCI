"""
@File : business_auto_create_report.py
@Date : 2021/11/2 10:36
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""

# 根据测试单号自动生成报告
import os
from fastapi import APIRouter
from app.models.test_task_model import get_by_id, get_build_details
from app.models.test_report_model import TestReportModel, create
from app.models.bug_model import get_testtask_related_bug, get_testtask_bug_statistics, calculate_in_value, \
	evaluate_grade, release_evaluation
from app.schemas import test_report_schemas
from app.utils import response_code, generate_report_summary_html
from app.config import TEST_REPORT_TEMPLATE

REPORT_TEMPLATE_PATH = r'D:\Python\Project\pythonProject\TomTawCI\app\static\reportSummary.html'
# REPORT_TEMPLATE_PATH = os.path.join(os.path.abspath(os.path.join(os.getcwd(), "..")), 'static', TEST_REPORT_TEMPLATE)


# 生成报告总结
def report_summary(task_id):
	summary_dict = dict()
	in_value = calculate_in_value(get_testtask_bug_statistics(task_id))
	summary_dict['build'] = get_build_details(task_id).get('name')  # 测试总结的标题使用
	summary_dict['testTime'] = '填写测试耗时.e.g. 1MD、0.5MD、3MH'
	summary_dict['testURL'] = '填写测试地址 e.g. http://test.ris.com'
	summary_dict['testClient'] = 'Win10Pro Core(TM) i5-7500 CPU 16G RAM、Chrome 版本 95.0.4638.69(根据实际情况填写客户机配置及浏览器版本)'
	summary_dict['testTools'] = 'DevTools'
	summary_dict['testTask'] = get_build_details(task_id).get('desc')
	summary_dict['riskEvaluation'] = "填写测试过程中未能规避的风险"
	summary_dict['summary'] = "对本次版本测试的总结"
	summary_dict['instabilityValue'] = in_value
	summary_dict['quality'] = evaluate_grade(in_value)
	summary_dict['if_release'] = release_evaluation(in_value)
	return summary_dict


def generate_report(task_id):
	"""根据测试单的状态判断能否生成"""
	task = get_by_id(task_id).to_dict()
	if task.get('status') == 'done':
		report_dict = dict()
		report_dict['product'] = task['product']
		report_dict['project'] = task['project']
		report_dict['tasks'] = task_id
		report_dict['owner'] = task['owner']
		report_dict['begin'] = task['begin']
		report_dict['end'] = task['end']
		report_dict['members'] = task['mailto']
		report_dict['title'] = '{0} TESTTASK#{1} {2} 测试报告'.format(task['end'], task['id'], task['name'])
		# report_dict['report'] = report_summary(task_id)
		report_dict['report'] = generate_report_summary_html.report_html2string(REPORT_TEMPLATE_PATH,
																				report_summary(task_id))
		report_dict['bugs'] = get_testtask_related_bug(task_id)
		report_dict['cases'] = ''
		report_dict['stories'] = ''
		report_dict['builds'] = task['build']
		report_dict['objectType'] = 'testtask'
		report_dict['objectID'] = task['id']
		report_dict['createdBy'] = task['owner']
	else:
		report_dict = dict()
	return report_dict


router = APIRouter(prefix="/ewordci/auto-report", tags=["auto-business"])


@router.post("/create", name="自动生成测试报告")
async def generate_test_report(task_id: int):
	report_dict = generate_report(task_id)  # 通过测试单号获取报告需要的信息
	report_schemas = test_report_schemas.TestReport(**report_dict)  # 传字典schema实例化
	db_test_report = TestReportModel(report_schemas.dict())  # 实例化数据模型
	create(db_test_report)  # 调用create插入数据库
	if db_test_report.id:  # 根据有没有生成新的id判断是否插入成功
		return response_code.resp_200(db_test_report.to_dict(), massage='测试单{}的测试报告生成成功'.format(task_id))
	else:
		return response_code.resp_400(message="生成报告失败")


if __name__ == "__main__":
	print(REPORT_TEMPLATE_PATH)
# print(generate_report(658))
# print(report_summary(658))
# print(report_summary(658))
