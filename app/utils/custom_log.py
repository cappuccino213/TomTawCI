"""
@File : custom_log.py
@Date : 2021/12/3 10:06
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""
from loguru import logger
from pathlib import Path
import time

# 获取项目跟路径
project_path = Path.cwd().parent
# 定义日志路径为:{项目根目录}/log
log_path = Path(project_path, 'log')
log_time = time.strftime('%Y%m%d')


class Logging:
	__instance = None
	logger.add(f"{log_path}/{log_time}.log", rotation="50MB", encoding="utf-8", enqueue=True, retention="10 days")

	# 参数定义参考 loguru官网 http://loguru.readthedocs.io/
	# https://cloud.tencent.com/developer/article/1849382?from=article.detail.1640693
	# https://cloud.tencent.com/developer/article/1664382
	def __new__(cls, *args, **kwargs):
		if not cls.__instance:
			cls.__instance = super(Logging, cls).__new__(cls, *args, **kwargs)

		return cls.__instance

	@classmethod
	def info(cls, msg):
		return logger.info(msg)

	@classmethod
	def debug(cls, msg):
		return logger.debug(msg)

	@classmethod
	def warning(cls, msg):
		return logger.warning(msg)

	@classmethod
	def error(cls, msg):
		return logger.error(msg)


logging = Logging()

if __name__ == "__main__":
	logging.info("中文test")
	logging.debug("中文test")
	logging.warning("中文test")
	logging.error("中文test")
