"""
@File : test_report_model.py
@Date : 2021/10/9 15:17
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""
from sqlalchemy import Column, Integer, Date, DateTime, Enum, String, Text
from app.db.database import Base
# from app.db.database import Session
from datetime import datetime
# from app.schemas import test_report_schemas


class TestReportModel(Base):
	__tablename__ = "zt_testreport"

	id = Column(Integer, autoincrement=True, primary_key=True, index=True)  # index=True表示是否创建索引
	product = Column(Integer)
	project = Column(Integer)
	tasks = Column(String(255))
	builds = Column(String(255))
	title = Column(String(255))
	begin = Column(Date)
	end = Column(Date)
	owner = Column(String(30))
	members = Column(Text)
	stories = Column(Text)
	bugs = Column(Text)
	cases = Column(Text)
	report = Column(Text)
	objectType = Column(String(20))
	objectID = Column(Integer)
	createdBy = Column(String(30))
	createdDate = Column(DateTime, default=datetime.now())
	deleted = Column(Enum('1', '0'), default='0')

	def __init__(self, fields_dict: dict):
		self.id = fields_dict.get('id')
		self.product = fields_dict.get('product')
		self.project = fields_dict.get('project')
		self.tasks = fields_dict.get('tasks')
		self.builds = fields_dict.get('builds')
		self.title = fields_dict.get('title')
		self.begin = fields_dict.get('begin')
		self.end = fields_dict.get('end')
		self.owner = fields_dict.get('owner')
		self.members = fields_dict.get('members')
		self.stories = fields_dict.get('stories')
		self.bugs = fields_dict.get('bugs')
		self.cases = fields_dict.get('cases')
		self.report = fields_dict.get('report')
		self.objectType = fields_dict.get('objectType')
		self.objectID = fields_dict.get('objectID')
		self.createdBy = fields_dict.get('createdBy')
		self.createdDate = fields_dict.get('createdDate')
		self.deleted = fields_dict.get('deleted')

	def to_dict(self):  # 用将数据列转换成dict
		return {column.name: getattr(self, column.name) for column in self.__table__.columns}


"""
# 根据id查询
def get(report_id: int):
	return Session.query(TestReportModel).filter(TestReportModel.id == report_id).all()


def get_by_id(report_id: int):
	return Session.query(TestReportModel).filter(TestReportModel.id == report_id).first()


# 新增数据
def create(testreport: test_report_schemas.TestReport):
	try:
		Session.add(testreport)
		Session.commit()
		Session.refresh(testreport)
	except Exception as e:
		print(str(e))
		Session.rollback()
		Session.flush()


# 更新数据
def update(testreport: test_report_schemas.TestReport):
	test_report = get_by_id(testreport.id)
	if test_report:
		update_dict = testreport.dict()
		try:
			for k, v in update_dict.items():
				setattr(test_report, k, v)  # setattr给对象的属性赋值 https://www.runoob.com/python/python-func-setattr.html
			Session.commit()
			Session.flush()
			Session.refresh(test_report)
			return test_report
		except Exception as e:
			print(str(e))
			Session.rollback()
			Session.flush()


# 逻辑删除
def remove(report_id: int):
	test_report = get_by_id(report_id)
	if test_report:
		try:
			setattr(test_report, 'deleted', '1')
			Session.commit()
			Session.flush()
			Session.refresh(test_report)
			return test_report
		except Exception as e:
			print(str(e))
			Session.rollback()
			Session.flush()
"""

if __name__ == "__main__":
	# print(get_by_id(325)['deleted'])
	# t = test_report_schemas.TestReportDel(id=556, deleted="1")
	from app.db.database import remove

	remove(555, TestReportModel)
