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
from app.models import build_model, release_model, user_model, team_model
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


def email_notice_rule(notice_type: str, business_id: int):
	"""
	根据不同的通知类型notice_type，用business_id去获取邮件信息
	:param notice_type: test_report,test_task,release
	:param business_id: 测试报告id，测试id，发布单id
	:return: z_mail函数需要的信息参数
	"""
	if notice_type == 'release':
		# 根据release_id获取release信息
		db_release = get(business_id, release_model.ReleaseModel)
		email_struct = dict(subject='【版本发布】 {}'.format(db_release.name), content_html=db_release.desc)
		email_struct['from'] = '张烨平 <1483029082@qq.com>'  # 因为from是python关键字所以只能通过这种方式赋值
		email_server = dict(account='1483029082@qq.com', password='lqmfvhxhzotdidjb')  # 之后需要传参 # TODO 需要考虑怎么传参
		email_to = user_model.get_user_email(dict(dept=4, account='zhangl'))  # 测试
		# email_to = user_model.get_user_email(dict(dept=5))  # 获取工程师邮件
		# 获取相关人员邮箱
		db_build = build_model.query_multiple_condition(dict(id=db_release.build))[0]
		team_infos = team_model.get_team_info(db_build.project)
		# email_cc = [(team['name'], team['email']) for team in team_infos]
		email_cc = [('九层风', '541159401@qq.com')]
		return dict(mail_struct=email_struct, mail_server=email_server, mail_to=email_to, mail_cc=email_cc)


@router.get("/mail", name="邮件通知")
async def email(notice_type: tools_schemas.EmailType, business_id: int):
	try:
		mail_info = email_notice_rule(notice_type, business_id)
		z_mail(mail_info['mail_struct'], mail_info['mail_server'], mail_info['mail_to'], mail_info['mail_cc'])
		return resp_200(dict(), message="邮件通知成功")
	except Exception as e:
		return resp_400(message="邮件通知失败，原因：{}".format(str(e)))


if __name__ == "__main__":
	mail_info = email_notice_rule('release', 237)
	z_mail(mail_info['mail_struct'], mail_info['mail_server'], mail_info['mail_to'], mail_info['mail_cc'])
