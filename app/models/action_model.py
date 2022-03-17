"""
@File : action_model.py
@Date : 2022/3/14 14:59
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""
# 系统日志表

from app.db.database import Base
from sqlalchemy import Column, Integer, String, Text, DateTime, Enum
import datetime


class ActionModel(Base):
	__tablename__ = "zt_action"

	id = Column(Integer, primary_key=True)
	objectType = Column(String)
	objectID = Column(Integer)
	product = Column(Integer)
	project = Column(Integer)
	actor = Column(String)
	action = Column(String)
	date = Column(DateTime)
	comment = Column(Text)
	extra = Column(Text)
	read = Column(Enum('0', '1'), default='0')
	efforted = Column(Integer, default=0)

	def __init__(self, fields_dict: dict):
		self.id = fields_dict.get('id')
		self.objectType = fields_dict.get('objectType')
		self.objectID = fields_dict.get('objectID')
		self.product = fields_dict.get('product')
		self.project = fields_dict.get('project')
		self.actor = fields_dict.get('actor')
		self.action = fields_dict.get('action')
		self.date = fields_dict.get('date')
		self.comment = fields_dict.get('comment')
		self.extra = fields_dict.get('extra')
		self.read = fields_dict.get('read')
		self.efforted = fields_dict.get('efforted')

	# 用将数据列转换成dict
	def to_dict(self):
		return {column.name: getattr(self, column.name) for column in self.__table__.columns}


# 创建日志记录的dict，用户创建测试单、报告单、发布单时的初始记录创建
def get_action_dict(object_type, object_id, product, project, actor, action):
	return dict(objectType=object_type, objectID=object_id, product=product, project=project, actor=actor,
				action=action, date=datetime.datetime.now(), comment='CI系统自动生成', extra='CI系统自动生成', read='0', efforted=0)


if __name__ == "__main__":
	ad = get_action_dict('testtask', 91, 1, 3, 'zyp', 'opened')
	print(ad)
