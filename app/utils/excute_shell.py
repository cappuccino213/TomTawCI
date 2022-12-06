"""
@File : excute_shell.py
@Date : 2022/6/16 16:55
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""

import subprocess

from app.utils.custom_log import logging


# 执行命令行函数
def run_shell(cli_str, if_log_info=True):
	"""
	:param cli_str: 命令行
	:param if_log_info: 当为False时不打印info日志，默认为True
	:return:
	"""
	try:
		logging.info(f"执行命令：{cli_str}")
		msg = subprocess.Popen(cli_str, stdout=subprocess.PIPE, universal_newlines=True, shell=True)
		stdout, stderr = msg.communicate()
		if if_log_info:
			logging.info(f"输出结果：{stdout}")
		return stdout
	except subprocess.SubprocessError as e:
		logging.error(f"执行异常：{str(e)}")
		raise str(e)


if __name__ == "__main__":
	pass
	run_shell('bz')
