"""
@File : tools_router.py
@Date : 2021/12/1 14:28
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""
# 常用工具的调用

from fastapi import APIRouter
from app.schemas import tools_schemas
from app.utils import compress
from app.utils.response_code import *
from app.utils.z_mail import z_mail
from app.models import test_task_model, test_report_model, build_model, release_model, user_model, team_model
from app.db.database import get

router = APIRouter(prefix="/ewordci/tools", tags=["tools"])


@router.get("/package", name="文件打包成*.7z")
def package(src_dir_path: str, dst_file_path: str, password='TomTaw@HZ'):
	try:
		compress.compress_to_7z(src_dir_path, dst_file_path, password)
		return resp_200(dict(), message="已将文件打包至{}".format(dst_file_path))
	except Exception as e:
		return resp_400(message="打包失败，原因{}".format(str(e)))


"""邮件通知规则"""


def email_notice_rule(notice_type: str, business_id: int, server_account: str, server_password: str,
					  email_accounts: list[str]):
	"""
	根据不同的通知类型notice_type，用business_id去获取邮件信息
	:param notice_type: test_report,test_task,release
	:param business_id: 测试报告id，测试id，发布单id
	:param server_password: 邮件服务器密码
	:param server_account: 邮件服务账号
	:param email_accounts: 手动发送发送人禅道账号
	:return: z_mail函数需要的信息参数dict形式
	"""
	email_server = dict(account=server_account, password=server_password)
	email_struct = {'from': '<{}>'.format(server_account)}  # 发件人显示
	email_to = []
	email_cc = []

	#  测试单
	if notice_type == 'test_task':
		db_test_task = get(business_id, test_task_model.TestTaskModel)
		email_struct = dict(subject=db_test_task.name, content_html=db_test_task.desc)
		email_to = user_model.get_user_email(dict(account=db_test_task.owner))
		if db_test_task.mailto:
			email_cc = user_model.get_user_email(dict(account=db_test_task.mailto.split(',')[1:]))

	# 测试报告
	elif notice_type == 'test_report':
		db_test_report = get(business_id, test_report_model.TestReportModel)
		email_struct = dict(subject=db_test_report.title, content_html=db_test_report.report)
		# 测试报告发送给项目组成员
		team_infos = team_model.get_team_info(db_test_report.project)
		email_to = [(team['name'], team['email']) for team in team_infos]
		# 抄给成员
		if db_test_report.members:
			email_cc = user_model.get_user_email(dict(account=db_test_report.members.split(',')[1:]))

	# 发布单邮件
	elif notice_type == 'release':
		# 根据release_id获取release信息
		db_release = get(business_id, release_model.ReleaseModel)
		email_struct = dict(subject='【版本发布】 {}'.format(db_release.name), content_html=db_release.desc)
		# 获取工程师地址
		email_to = user_model.get_user_email(dict(dept=5))
		# 获取相关人员邮箱
		db_build = build_model.query_build_multiple_condition(dict(id=db_release.build))[0]
		team_infos = team_model.get_team_info(db_build.project)
		email_cc = [(team['name'], team['email']) for team in team_infos]
	# 测试数据
	# email_to = user_model.get_user_email(dict(dept=4, account='zhangl'))  # 测试数据
	# email_cc = [('九层风', '541159401@qq.com')]

	# 是否手动通知即自己传邮箱的方式，ci客户端可表现为选择某一个用户
	elif notice_type == 'release_manual':
		db_release = get(business_id, release_model.ReleaseModel)
		email_struct = dict(subject='【版本发布】 {}'.format(db_release.name), content_html=db_release.desc)
		# 获取OEM工程师邮件
		if email_accounts:  # 防止没有传账号时，发送给所有人
			email_to = user_model.get_user_email(dict(account=email_accounts))
		# 获取相关人员邮箱
		db_build = build_model.query_build_multiple_condition(dict(id=db_release.build))[0]
		team_infos = team_model.get_team_info(db_build.project)
		email_cc = [(team['name'], team['email']) for team in team_infos]
	# email_cc = [("张烨平", "1483029082@qq.com")]

	return dict(mail_struct=email_struct, mail_server=email_server, mail_to=email_to, mail_cc=email_cc)


@router.post("/mail", name="邮件通知")
async def email(param: tools_schemas.EmailNotice):
	try:
		email_info = email_notice_rule(param.notice_type, param.business_id, param.server_account,
									   param.server_password, param.email_to)
		z_mail(email_info['mail_struct'], email_info['mail_server'], email_info['mail_to'], email_info['mail_cc'])
		return resp_200(dict(), message="邮件通知成功")
	except Exception as e:
		return resp_400(message="邮件通知失败，原因：{}".format(str(e)))


if __name__ == "__main__":
	mail_info = email_notice_rule('release', 239, '1483029082@qq.com', 'lqmfvhxhzotdidjb')
	z_mail(mail_info['mail_struct'], mail_info['mail_server'], mail_info['mail_to'], mail_info['mail_cc'])
