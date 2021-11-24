"""
@File : config.py
@Date : 2021/10/9 15:06
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""

"""数据库配置"""
# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:123456@192.168.1.16:3306/zentao"
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://test:123456@192.168.1.43:3306/zentao"


"""CI相关配置"""
# 为了参数import时方便，用dict来管理各自相关的参数集
# 自动提测
APPLY_TEST = {}

# 自动报告
AUTO_TEST_REPORT = {
	"TEMPLATE": 'reportSummary.html'
}

# 自动发布
AUTO_DISTRIBUTE = {}

"""CD相关配置"""

if __name__ == "__main__":
	pass
