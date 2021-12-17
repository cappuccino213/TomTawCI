"""
@File : log_handle.py
@Date : 2021/12/14 21:20
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""
import logging
from pprint import pformat
from loguru import logger

# 参考链接
# https://blog.csdn.net/qq_29622543/article/details/115655275


# 日志格式
LOG_FORMAT = '<green>{time:YYYY-MM-DD HH:mm:ss,SSS}</green> <level>{level: <2}</level> - <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>'


class InterceptHandler(logging.Handler):
	def emit(self, record):
		# Get corresponding Loguru level if it exits
		try:
			level = logger.level(record.levelname).name
		except ValueError:
			level = record.levelno

		# Find caller from where originated the logged message
		frame, depth = logging.currentframe(), 2
		while frame.f_code.co_filename == logging.__file__:
			frame = frame.f_back
			depth += 1

		logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def format_record(record: dict) -> str:
	"""   Custom format for loguru loggers.
    Uses pformat for log any data like request/response body during debug.
    Works with logging if loguru handler it.

    Example:
    # >>> payload = [{"users":[{"name": "Nick", "age": 87, "is_active": True}, {"name": "Alex", "age": 27, "is_active": True}], "count": 2}]
    # >>> logger.bind(payload=).debug("users payload")
    # >>> [   {   'count': 2,
    # >>>         'users': [   {'age': 87, 'is_active': True, 'name': 'Nick'},
    # >>>                      {'age': 27, 'is_active': True, 'name': 'Alex'}]}]
    """
	format_string = LOG_FORMAT

	if record["extra"].get("payload") is not None:
		record["extra"]["payload"] = pformat(
			record["extra"]["payload"], indent=4, compact=True, width=88
		)
		format_string += "\n<level>{extra[payload]}</level>"

	format_string += "{exception}\n"
	return format_string


if __name__ == "__main__":
	pass
