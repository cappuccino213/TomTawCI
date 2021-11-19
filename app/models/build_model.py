"""
@File : build_model.py
@Date : 2021/11/19 11:02
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""
from app.db.database import Base
from sqlalchemy import Column, Integer, String, Date, Text, Enum


# 版本信息
class BuildModel(Base):
	__tablename__ = "zt_build"

	id = Column(Integer, primary_key=True)
	name = Column(String(150))
	branch = Column(Integer)
	product = Column(Integer)
	project = Column(Integer)
	scmPath = Column(String(255))
	filePath = Column(String(255))
	date = Column(Date)
	stories = Column(Text)
	bugs = Column(Text)
	builder = Column(String(30))
	desc = Column(Text)
	deleted = Column(Enum('0', '1'))

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


"""
调用统一的CRUD操作，此处不用再定义
# 根据id查询
def get(build_id: int):
	return Session.query(BuildModel).filter(BuildModel.id == build_id).all()


def get_by_id(build_id: int):
	return Session.query(BuildModel).filter(BuildModel.id == build_id).first()
"""

if __name__ == "__main__":
	from app.db.database import get

	print(get(609, BuildModel, ).to_dict())
