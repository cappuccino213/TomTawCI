"""
@File : release_model.py
@Date : 2021/11/29 17:03
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""
from app.db.database import Base, Session
from sqlalchemy import Column, Integer, String, Text, Enum, Date
from datetime import date
from sqlalchemy import desc


# 发布单
class ReleaseModel(Base):
	__tablename__ = "zt_release"

	id = Column(Integer, primary_key=True)
	product = Column(Integer)
	branch = Column(Integer, default=0)
	build = Column(Integer)
	name = Column(String(255))
	marker = Column(Enum('0', '1'), default='0')  # 是否里程碑
	date = Column(Date, default=date.today())  # 发布日期，一定要传值
	stories = Column(Text, default='')  # 完成的需求
	bugs = Column(Text, default='')  # 解决的bugs
	leftBugs = Column(Text, default='')  # 遗留的bugs
	desc = Column(Text, default='发布描述信息')
	status = Column(String(20), default='normal')
	subStatus = Column(String(30), default='')
	deleted = Column(Enum('0', '1'), default='0')

	def __init__(self, fields_dict: dict):
		self.id = fields_dict.get('id')
		self.product = fields_dict.get('product')
		self.branch = fields_dict.get('branch')
		self.build = fields_dict.get('build')
		self.name = fields_dict.get('name')
		self.marker = fields_dict.get('maker')  # 是否里程碑
		self.date = fields_dict.get('date')  # 发布日期
		self.stories = fields_dict.get('stories')  # 完成的需求
		self.bugs = fields_dict.get('stories')  # 解决的bugs
		self.leftBugs = fields_dict.get('leftBugs')  # 遗留的bugs
		self.desc = fields_dict.get('desc')
		self.status = fields_dict.get('status')
		self.subStatus = fields_dict.get('subStatus')
		self.deleted = fields_dict.get('deleted')

	def to_dict(self):
		return {column.name: getattr(self, column.name) for column in self.__table__.columns}


# 筛选出各产品中最后发布的版本
def query_by_product(product_id: int):
	return Session.query(ReleaseModel).filter(ReleaseModel.product == product_id, ReleaseModel.deleted == '0').order_by(
		desc(ReleaseModel.id)).first()



if __name__ == "__main__":
	print(query_by_product(7).to_dict())
