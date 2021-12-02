"""
@File : team_models.py
@Date : 2021/11/30 15:01
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""
from app.db.database import Base, Session
from sqlalchemy import Column, Integer, String, Text, Enum, Date, Float, DECIMAL


# 项目、任务的团队成员
class TeamModel(Base):
	__tablename__ = "zt_team"

	id = Column(Integer, primary_key=True)
	root = Column(Integer)
	type = Column(Enum('project', 'task'))
	account = Column(String(30))
	role = Column(String(30))
	limited = Column(String(8))
	join = Column(Date)
	days = Column(Integer)
	hours = Column(Float)
	estimate = Column(DECIMAL)
	consumed = Column(DECIMAL)
	left = Column(DECIMAL)
	order = Column(Integer)

	def to_dict(self):
		return {column.name: getattr(self, column.name) for column in self.__table__.columns}


# 根据项目id查询团队
def query_by_project(project_id):
	return Session.query(TeamModel).filter(TeamModel.root == project_id).all()


if __name__ == "__main__":
	print(TeamModel().query_by_project(66).to_dict())
