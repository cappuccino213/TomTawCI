"""
@File : ci_server_model.py
@Date : 2022/5/18 15:13
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""
from app.db.database import Base, Session
from app.utils.custom_log import *

from sqlalchemy import Column, Integer, String, Enum


# 服务器管理
class ServerModel(Base):
	__tablename__ = "ci_server"

	id = Column(Integer, primary_key=True, autoincrement=True)
	ipAddress = Column(String(30))
	serverName = Column(String(100))
	remark = Column(String(512))
	deleted = Column(Enum('0', '1'), default='0')

	def __init__(self, fields_dict: dict):
		self.id = fields_dict.get('id')
		self.ipAddress = fields_dict.get('ipAddress')
		self.serverName = fields_dict.get('serverName')
		self.remark = fields_dict.get('remark')
		self.deleted = fields_dict.get('deleted')

	def to_dict(self):
		return {column.name: getattr(self, column.name) for column in self.__table__.columns}


# 获取列表
def get_server_list(models: Base):
	try:
		data = Session.query(models).filter(models.deleted == '0').all()
		return [col.to_dict() for col in data]
	except Exception as e:
		logging.error(str(e))
	finally:
		Session.close()


# 根据ip查询记录
def if_ip_exist(ip, models: Base):
	try:
		data = Session.query(models).filter(models.deleted == '0', models.ipAddress == ip).all()
		return [col.to_dict() for col in data]
	except Exception as e:
		logging.error(str(e))
	finally:
		Session.close()


if __name__ == "__main__":
	# logging.info(get_server_list(ServerModel))
	logging.info(if_ip_exist('192.168.1.19',ServerModel))
