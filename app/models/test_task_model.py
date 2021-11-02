"""
@File : test_task_model.py
@Date : 2021/11/2 9:30
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""
from app.db.database import Base
from sqlalchemy import Column, String, Integer, Date, Enum, Text
from app.db.database import Session


class TestTaskModel(Base):
	__tablename__ = "zt_testtask"

	id = Column(Integer, primary_key=True)
	name = Column(String(90))
	product = Column(Integer)
	project = Column(Integer)
	build = Column(String(30))
	owner = Column(String(30))
	pri = Column(Integer)
	begin = Column(Date)
	end = Column(Date)
	mailto = Column(Text)
	desc = Column(Text)
	status = Column(Enum('blocked', 'doing', 'wait', 'done'))
	deleted = Column(Enum('0', '1'))

	def __init__(self):
		pass

	# 用将数据列转换成dict
	def to_dict(self):
		return {column.name: getattr(self, column.name) for column in self.__table__.columns}


# 通过id获取测试单
def get_by_id(task_id: int):
	return Session.query(TestTaskModel).filter(TestTaskModel.id == task_id).first()


# 新增
def create():
	pass


# 修改
def update():
	pass


# 删除
def remove():
	pass


if __name__ == "__main__":
	print(get_by_id(245).to_dict().get('status'))
