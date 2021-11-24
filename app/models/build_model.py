"""
@File : build_model.py
@Date : 2021/11/19 11:02
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""
from app.db.database import Base, Session
from sqlalchemy import Column, Integer, String, Date, Text, Enum
from sqlalchemy import desc
from datetime import date


# 版本信息
class BuildModel(Base):
	__tablename__ = "zt_build"

	id = Column(Integer, primary_key=True)
	name = Column(String(150))
	branch = Column(Integer, default=0)
	product = Column(Integer)
	project = Column(Integer)
	scmPath = Column(String(255))
	filePath = Column(String(255))
	date = Column(Date, default=date.today())
	stories = Column(Text, default='')
	bugs = Column(Text, default='')
	builder = Column(String(30))
	desc = Column(Text)
	deleted = Column(Enum('0', '1'), default='0')

	def __init__(self, fields_dict: dict):
		self.id = fields_dict.get('id')
		self.name = fields_dict.get('name')
		self.branch = fields_dict.get('branch')
		self.product = fields_dict.get('product')
		self.project = fields_dict.get('project')
		self.scmPath = fields_dict.get('scmPath')
		self.filePath = fields_dict.get('filePath')
		self.date = fields_dict.get('date')
		self.bugs = fields_dict.get('bugs')
		self.builder = fields_dict.get('builder')
		self.stories = fields_dict.get('stories')
		self.desc = fields_dict.get('desc')
		self.deleted = fields_dict.get('deleted')

	def to_dict(self):
		return {column.name: getattr(self, column.name) for column in self.__table__.columns}


# 根据项目ID获取最新的版本号
def query_by_project(project_id: int):
	return Session.query(BuildModel).filter(BuildModel.project == project_id, BuildModel.deleted == '0').order_by(
		desc(BuildModel.date)).first()


# 多条件查询版本信息
def query_multiple_condition(condition: dict):
	result = Session.query(BuildModel).filter(BuildModel.deleted == '0')
	if condition.get('product'):
		result = result.filter(BuildModel.product == condition.get('product'))
	if condition.get('project'):
		result = result.filter(BuildModel.project == condition.get('project'))
	if condition.get('name'):
		result = result.filter(BuildModel.name == condition.get('name'))
	if condition.get('date'):
		result = result.filter(BuildModel.gender == condition.get('date'))
	return result.all()


if __name__ == "__main__":
	pass
	d = {
		"product": "7",
		"project": "66",
		"name": "v1.0.0.1(版本名称)"
	}
	print(query_multiple_condition(d))
