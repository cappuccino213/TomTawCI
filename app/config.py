"""
@File : config.py
@Date : 2021/10/9 15:06
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""

"""数据库配置"""
# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:123456@192.168.1.16:3306/zentao"
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://test:123456@192.168.1.43:3306/zentao"


"""禅道API地址"""
ZENTAO_URL = "http://192.168.1.43:8089"

if __name__ == "__main__":
	pass
