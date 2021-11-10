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


"""与测试单相关的函数"""


# 通过测试单号获取版本详情
def get_build_details(task_id):
	cur_res = Session.execute(
		'SELECT * FROM zt_build WHERE id in (SELECT build FROM zt_testtask WHERE id = :id)', {'id': task_id})
	res_list = cur_res.first()
	return res_list._mapping   # 返回字典项

if __name__ == "__main__":
	# print(get_by_id(245).to_dict().get('status'))
	print(get_build_details(643))
