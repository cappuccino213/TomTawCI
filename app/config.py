"""
@File : config.py
@Date : 2021/10/9 15:06
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""

from pathlib import Path
import time

"""数据库配置"""
DATABASE_CONFIGURE = {
	# "SQLALCHEMY_DATABASE_URL": "mysql+pymysql://root:123456@localhost:3306/zentao",  # 链接
	"SQLALCHEMY_DATABASE_URL": "mysql+pymysql://test:123456@192.168.1.43:3306/zentao",  # 链接
	"SQL_ECHO": False  # 是否输出执行语句
}

"""CI相关配置"""
# 项目根目录
ROOT_DIRECTORY = Path(Path.cwd(), 'app').resolve()  # 从main函数运行，目录刚好到app层
# pathlib路径操作可以参考
# https://zhuanlan.zhihu.com/p/139783331

# 为了参数import时方便，用dict来管理各自相关的参数集
# 自动提测
APPLY_TEST = {'TEMPLATE': 'testTaskDesc.html'}

# 自动报告
AUTO_TEST_REPORT = {
	'TEMPLATE': 'reportSummary.html'
}

# 自动发布
AUTO_DISTRIBUTE = {
	'TEMPLATE': 'releaseDesc.html',
	'COMPRESS_PATH': r'\\192.168.1.19\distribution'

}
"""CD相关配置"""
# CD客户端参数（用于CD客户端信息的全局缓存，避免文件读取IO的问题）

# CD_CLIENT_INFO = read_json('./static/CDClientInfo.json')

"""工具类配置"""
# 邮件配置 用的z_mail暂时不需要这个配置
MAIL_CONFIG = {
	'MAIL_SERVER': 'smtp.qq.com',
	'PORT': 465
}

# 日志配置
# fastapi的日志配置main函数的运行日志配置，其他模块的运行日志单独在custom_log中配置
LOG_CONFIG = {
	'IF_DEBUG': True,
	'LOG_PATH': Path.home().joinpath(ROOT_DIRECTORY, f'logs\\start_{time.strftime("%Y%m%d")}.log'),
	'ROTATION': '0:00',  # 每个日志多大
	# 'ROTATION': '10 MB',  # 每个日志多大
	'RETENTION': '1 week'  # 保留时长
}
# logger.add("file_1.log", rotation="500 MB")  # 自动循环过大的文件
# logger.add("file_2.log", rotation="12:00")  # 每天中午创建新文件
# logger.add("file_3.log", rotation="1 week")  # 一旦文件太旧进行循环

"""运行参数配置"""
RUN_CONFIGURE = {
	"PORT": 8889,  # 端口号
	"RELOAD": True,  # 是否重载代码，调试使用
	"DEBUG": True,  # 是否开启调试
	"WORKERS": 4
}

# 更多参数详见\TomTawCI\venv\Lib\site-packages\uvicorn\main.py
if __name__ == "__main__":
	# print(LOG_CONFIG)
	pass
