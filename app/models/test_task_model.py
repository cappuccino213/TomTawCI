"""
@File : test_task_model.py
@Date : 2021/11/2 9:30
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""
from app.db.database import Base
from sqlalchemy import Column, String, Integer, Date, Enum, Text
from app.db.database import Session
from datetime import date


class TestTaskModel(Base):
	__tablename__ = "zt_testtask"

	id = Column(Integer, primary_key=True)
	name = Column(String(90))
	product = Column(Integer)
	project = Column(Integer)
	build = Column(String(30))
	owner = Column(String(30))
	pri = Column(Integer, default=2)
	begin = Column(Date, default=date.today())
	end = Column(Date, default=date.today())
	mailto = Column(Text)
	desc = Column(Text)
	report = Column(Text, default='CI')  # 数据库中为非空字段给个默认值
	auto = Column(String(10), default='no')
	subStatus = Column(String(30), default='NA')
	status = Column(Enum('blocked', 'doing', 'wait', 'done'),default='wait')
	deleted = Column(Enum('0', '1'), default='0')

	def __init__(self, fields_dict: dict):
		self.id = fields_dict.get('id')
		self.name = fields_dict.get('name')
		self.product = fields_dict.get('product')
		self.project = fields_dict.get('project')
		self.build = fields_dict.get('build')
		self.owner = fields_dict.get('owner')
		self.pri = fields_dict.get('pri')
		self.begin = fields_dict.get('begin')
		self.end = fields_dict.get('end')
		self.mailto = fields_dict.get('mailto')
		self.desc = fields_dict.get('desc')
		self.status = fields_dict.get('status')
		self.deleted = fields_dict.get('deleted')

	# 用将数据列转换成dict
	def to_dict(self):
		return {column.name: getattr(self, column.name) for column in self.__table__.columns}


"""
调用统一的CRUD操作，此处不用再定义
# 通过id获取测试单
def get_by_id(task_id: int):
	return Session.query(TestTaskModel).filter(TestTaskModel.id == task_id).first()


# 新增
def create(test_task: test_task_schemas.TestTask):
	try:
		Session.add(test_task)
		Session.commit()
		Session.refresh(test_task)
	except Exception as e:
		print(str(e))
		Session.rollback()
		Session.flush()

"""

"""与测试单相关的函数"""


# 通过测试单号获取版本详情
def get_build_details(task_id):
	cur_res = Session.execute(
		'SELECT * FROM zt_build WHERE id in (SELECT build FROM zt_testtask WHERE id = :id)', {'id': task_id})
	res_list = cur_res.first()
	return res_list._mapping  # 返回字典项


if __name__ == "__main__":
	# print(get_by_id(245).to_dict().get('status'))
	print(get_build_details(643))
