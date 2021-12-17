"""
@File : team_model.py
@Date : 2021/11/30 15:01
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""
from app.db.database import Base, Session
from sqlalchemy import Column, Integer, String, Enum, Date, Float, DECIMAL
from app.db.database import execute_sql
from app.utils.custom_log import *


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
	try:
		return Session.query(TeamModel).filter(TeamModel.root == project_id).all()
	except Exception as e:
		logging.error(str(e))
	finally:
		Session.close()


# 获取团队的真实姓名、email
def get_team_info(project_id: int):
	try:
		sql_statement = """
		SELECT
		zt.`root` AS project,
		zt.role,
		zt.account,
		zu.`realname` as `name`,
		zu.email 
	FROM
		zt_team zt
		LEFT JOIN zt_user zu ON zt.`account` = zu.`account` 
	WHERE
		zt.`type` = 'project' 
		AND zu.deleted = '0'
		AND zt.`root`={}
		""".format(project_id)
		return execute_sql(sql_statement)
	except Exception as e:
		logging.error(str(e))
	finally:
		Session.close()


if __name__ == "__main__":
	# print(TeamModel().query_by_project(66).to_dict())
	# print(get_team_info(81))
	team_infos = get_team_info(81)
	print([(team['name'], team['email']) for team in team_infos])
