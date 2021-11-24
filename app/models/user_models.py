"""
@File : user_models.py
@Date : 2021/11/23 16:33
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""
from app.db.database import Base, Session
from sqlalchemy import Column, Integer, String, Enum


# 版本信息
class UserModel(Base):
	__tablename__ = "zt_user"

	id = Column(Integer, autoincrement=True, primary_key=True)
	dept = Column(Integer)
	account = Column(String(30), unique=True)
	password = Column(String(32))
	role = Column(String(10))
	realname = Column(String(100))
	nickname = Column(String(60))
	gender = Column(Enum('f', 'm'))
	mobile = Column(String(11))
	email = Column(String(90))
	qq = Column(String(20))
	address = Column(String(120))
	deleted = Column(Enum('0', '1'))

	def __init__(self, fields_dict: dict):
		self.id = fields_dict.get('id')
		self.dept = fields_dict.get('dept')
		self.account = fields_dict.get('account')
		self.password = fields_dict.get('password')
		self.role = fields_dict.get('role')
		self.realname = fields_dict.get('realname')
		self.nickname = fields_dict.get('nickname')
		self.gender = fields_dict.get('gender')
		self.mobile = fields_dict.get('mobile')
		self.email = fields_dict.get('email')
		self.qq = fields_dict.get('qq')
		self.address = fields_dict.get('address')
		self.deleted = fields_dict.get('deleted')

	def to_dict(self):
		return {column.name: getattr(self, column.name) for column in self.__table__.columns}


# 按角色筛选用户
def query_by_dept(dept_value: str):
	return Session.query(UserModel).filter(UserModel.dept == dept_value, UserModel.deleted == '0').all()


# 多条件查询用户
def query_multiple_condition(condition: dict):
	result = Session.query(UserModel).filter(UserModel.deleted == '0')
	if condition.get('account'):
		result = result.filter(UserModel.account == condition.get('account'))
	if condition.get('dept'):
		result = result.filter(UserModel.dept == condition.get('dept'))
	if condition.get('role'):
		result = result.filter(UserModel.role == condition.get('role'))
	if condition.get('gender'):
		result = result.filter(UserModel.gender == condition.get('gender'))
	return result.all()


if __name__ == "__main__":
	pass
