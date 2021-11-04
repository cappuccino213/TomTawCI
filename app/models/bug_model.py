"""
@File : bug_model.py
@Date : 2021/10/12 16:06
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""
from sqlalchemy import Column, Integer, String, Enum, DateTime, Date
from app.db.database import Base
from app.db.database import Session


class BugModel(Base):
	__tablename__ = "zt_bug"

	id = Column(Integer, primary_key=True)
	product = Column(Integer)
	project = Column(Integer)
	story = Column(Integer)
	task = Column(Integer)
	title = Column(String)
	severity = Column(Integer)
	pri = Column(Integer)
	type = Column(String)
	status = Column(Enum('active', 'resolved', 'closed'))
	openedBy = Column(String)
	openedDate = Column(DateTime)
	assignedTo = Column(String)
	assignedDate = Column(DateTime)
	closedBy = Column(String)
	closedDate = Column(DateTime)
	deadline = Column(Date)
	testtask = Column(Integer)  # 测试单
	resolvedBy = Column(String)  # 解决人
	resolution = Column(String)  # 解决方案
	resolvedBuild = Column(String)  # 解决版本
	resolvedDate = Column(DateTime)  # 解决日期
	deleted = Column(Enum('0', '1'))


"""bug的CRUD"""


# 根据测试单号获取关联的bug的id，用,隔开
def get_testtask_related_bug(task_id):
	cur_res = Session.execute(
		'SELECT id FROM zt_bug WHERE openedBuild IN (SELECT build FROM zt_testtask WHERE id = :id)', {'id': task_id})
	res_list = cur_res.all()
	id_list = [str(res[0]) for res in res_list]
	return ','.join(id_list)


def get_by_id(bug_id):
	return Session.query(BugModel).filter(BugModel.id == bug_id).first()


"""bug相关的评估函数"""


# 不稳定系数（instability）IN值计算
def calculate_in_value(severity: dict[str:int]):
	# fatal: int, severe: int, mistake: int, suggest: int
	return severity['fatal'] * 30 + severity['severe'] * 15 + severity['mistake'] * 5 + severity['suggest'] * 1


# 提测质量评估，根据in值计算
def evaluate_grade(in_value: int):
	if in_value >= 30:
		return '不合格'
	elif in_value >= 15:
		return '合格'
	elif in_value >= 10:
		return '良好'
	else:
		return '优秀'


# 版本发布评估
def release_evaluation(in_value: int):
	if in_value < 15:
		return '允许发布'
	else:
		return '不予发布'


if __name__ == "__main__":
	# bug_num = {'fatal': 0, 'severe': 1, 'mistake': 2, 'suggest': 3}
	# ins_value = calculate_in_value(bug_num)
	# print(ins_value)
	# print(evaluate_grade(ins_value))
	# print(release_evaluation(ins_value))

	print(get_testtask_related_bug(658))
