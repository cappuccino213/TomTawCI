"""
@File : business_auto_create_report.py
@Date : 2021/11/2 10:36
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""

# 根据测试单号自动生成报告

from fastapi import APIRouter
from app.models.test_task_model import *


# 生成报告总结
def report_summary():
	pass


def generate_report(task_id):
	"""根据测试单的状态判断能否生成"""
	task = get_by_id(task_id).to_dict()
	if task.get('status') == 'done':
		report_dict = dict()
		report_dict['owner'] = task['owner']
		report_dict['begin'] = task['begin']
		report_dict['end'] = task['end']
		report_dict['mailto'] = task['members']
		report_dict['title'] = '{0} TESTTASK#{1} {2} 测试报告'.format(task['end'], task['id'], task['title'])
		report_dict['report'] = ''
		report_dict['bugs'] = task['bugs']
		report_dict['cases'] = ''
		report_dict['stories'] = ''
		report_dict['build'] = task['build']
		report_dict['objectType'] = 'testtask'
		report_dict['objectID'] = task['id']
		report_dict['createdBy'] = task['owner']


	else:
		pass


router = APIRouter(prefix="/ewordci/auto-create-report", tags=["auto-business"])


@router.post("/post", name="自动生成测试报告")
async def generate_test_report(task_id: int):
	pass


if __name__ == "__main__":
	pass
