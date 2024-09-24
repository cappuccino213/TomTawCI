"""
@File : z_mail.py
@Date : 2021/12/7 16:15
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""
import smtplib

import zmail
from utils.custom_log import logging

def z_mail(mail_struct: dict, mail_server: dict, mail_to: [list, str], mail_cc: [list, str]):
	"""
	通过zmail库发送邮件，参考地址
	https://github.com/zhangyunhao116/zmail/blob/master/README-cn.md
	:param mail_struct: 邮件结构 {'subject':'主题',
								'from':'发送人'，例如'from':'Boss <mymail@foo.com>',
								'content_text':'邮件文本内容'，
								'content_html':'邮件html内容',
								'attachments':'邮件附件'例如 '/User/apple/1.txt' or ['/User/apple/1.txt','2.txt'] or [('1.txt',b'...'),('2.txt',b'...')] )}
	:param mail_server:邮件服务器{'account':邮件地址,'password':邮件密码}
	:param mail_to:发送地址'yourfriend@example.com'或者['yourfriend1@example.com','yourfriend2@example.com']
	:param mail_cc:抄送地址[('Boss','bar@163.com'),'bar@126.com']也可以为他们命名(使用元组，第一个为其命名，第二个为其地址)
	:return:
	"""
	# server = zmail.server(mail_server['account'], mail_server['password'])
	# return server.send_mail(mail_to, mail_struct, cc=mail_cc)
	logging.info("正在连接邮件服务器...")
	server = zmail.server(mail_server['account'], mail_server['password'])
	logging.info("成功连接邮件服务器.")

	try:
		logging.info("正在发送邮件...")
		server.send_mail(mail_to, mail_struct, cc=mail_cc)
		msg = "邮件发送成功."
		logging.info(msg)
		return msg
	except smtplib.SMTPResponseException as e:
		ecp_msg = f"邮件服务器发生错误（一般见于qq邮箱服务错误，邮件也可能发送成功）: {e}"
		logging.error(ecp_msg)
		return ecp_msg
		# raise
	except Exception as e:
		logging.error(f"邮件发送失败: {e}")
		# raise
		return None




if __name__ == "__main__":

	test_mail_1 = {'from': 'zyp <1483029082@qq.com>',
		'subject': '测试邮件','content_html':'这是邮件内容'}

	test_server = {'account':'1483029082@qq.com', 'password':'lqmfvhxhzotdidjb'}
	# test_server ={'account':'yeahcheung213@163.com', 'password':'EZaXXzFcMQXV5Fw8'}

	test_to = ['541159401@qq.com',]
	test_cc = [('zyp', '1483029082@qq.com')]
	z_mail(test_mail_1, test_server, test_to, test_cc)
