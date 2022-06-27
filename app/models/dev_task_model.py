"""
@File : dev_task_model.py
@Date : 2022/6/24 10:34
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""
import datetime

from sqlalchemy import Column, Integer, String, Enum, DateTime, Date, SmallInteger, Float

from app.db.database import Base
from app.db.database import Session
from app.utils.custom_log import *


class DevTaskModel(Base):
	__tablename__ = "zt_task"

	id = Column(Integer, primary_key=True)
	parent = Column(Integer)
	project = Column(Integer)
	module = Column(Integer)
	story = Column(Integer)
	storyVersion = Column(SmallInteger)
	fromBug = Column(Integer)
	name = Column(String)
	type = Column(String)
	pri = Column(SmallInteger)
	estimate = Column(Float)
	consumed = Column(Float)
	left = Column(Float)
	deadline = Column(Date)
	status = Column(Enum('wait', 'doing', 'done', 'pause', 'cancel', 'closed'))
	subStatus = Column(String)
	color = Column(String)
	mailto = Column(String)
	desc = Column(String)
	openedBy = Column(String)
	openedDate = Column(DateTime)
	assignedTo = Column(String)
	assignedDate = Column(DateTime)
	estStarted = Column(Date)
	realStarted = Column(DateTime)
	finishedBy = Column(String)
	finishedDate = Column(DateTime)
	finishedList = Column(String)
	canceledBy = Column(String)
	canceledDate = Column(DateTime)
	closedBy = Column(String)
	closedDate = Column(DateTime)
	closedReason = Column(String)
	lastEditedBy = Column(String)
	lastEditedDate = Column(DateTime)
	deleted = Column(Enum('0', '1'))

	def to_dict(self):
		return {column.name: getattr(self, column.name) for column in self.__table__.columns}


"""开发任务的CRUD"""


# 根据项目、状态、指派给、指派时间等条件获取bug的列表
def query_dev_task_list(condition: dict):
	"""
	:param condition: project、status、assignedTo、timeRange（时间范围/天，与指派时间比较），etc.
	:return: bug list
	"""
	try:
		result = Session.query(DevTaskModel).filter(DevTaskModel.deleted == '0')
		if condition.get('project'):
			result = result.filter(DevTaskModel.project == condition.get('project'))
		if condition.get('status'):
			result = result.filter(DevTaskModel.status == condition.get('status'))
		if condition.get('assignedTo'):
			result = result.filter(DevTaskModel.assignedTo == condition.get('assignedTo'))
		# 指派时间几天内
		if condition.get('timeRange'):
			result = result.filter(DevTaskModel.assignedDate >= (datetime.datetime.now() - datetime.timedelta(days=condition.get('timeRange'))))
		return result.all()
	except Exception as e:
		logging.error(str(e))
	finally:
		Session.close()


if __name__ == "__main__":
	task_list = query_dev_task_list({"project": 35, "status": "done", "assignedTo": "hyp", "timeRange": 7})
	print([task.to_dict() for task in task_list])
