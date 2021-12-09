"""
@File : config.py
@Date : 2021/10/9 15:06
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""

from pathlib import Path

"""数据库配置"""
DATABASE_CONFIGURE = {
	# "SQLALCHEMY_DATABASE_URL": "mysql+pymysql://root:123456@localhost:3306/zentao",  # 链接
	"SQLALCHEMY_DATABASE_URL": "mysql+pymysql://test:123456@192.168.1.43:3306/zentao",  # 链接
	"SQL_ECHO": True  # 是否输出执行语句
}

"""CI相关配置"""
# 项目根目录
# ROOT_DIRECTORY = r'D:\Python\Project\pythonProject\TomTawCI\app'
ROOT_DIRECTORY = Path(Path.cwd(), 'app')  # 从main函数运行，目录刚好到app层

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

"""工具类配置"""
# 邮件配置
MAIL_CONFIG = {
	'MAIL_SERVER': 'smtp.qq.com',
	'PORT': 465
}

# 日志配置

"""运行参数配置"""
RUN_CONFIGURE = {
	"PORT": 8889,  # 端口号
	"RELOAD": True,  # 是否重载代码，调试使用
	"DEBUG": True,  # 是否开启调试
	"WORKERS": 4
}

# 更多参数详见\TomTawCI\venv\Lib\site-packages\uvicorn\main.py
if __name__ == "__main__":
	print(ROOT_DIRECTORY)
