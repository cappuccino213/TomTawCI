"""
@File : user_model.py
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


# 根据部门、姓名、用户获取用户邮件信息
def get_user_email(condition: dict) -> list[tuple]:
	"""
	:param condition: 单值{'dept':5,'account':'fmf','realname':'方敏芳'}
	:param condition: 或者批量{'dept':5,'account':['fmf','qianq'],'realname':['方敏芳','钱迁']}
	:return:[('方敏芳','1661886732@qq.com'),('钱迁','360309531@qq.com')]
	"""
	result = Session.query(UserModel).filter(UserModel.deleted == '0')
	if condition.get('dept'):
		if isinstance(condition.get('dept'), int):
			result = result.filter(UserModel.dept == condition.get('dept'))
		if isinstance(condition.get('dept'), list):
			result = result.filter(UserModel.dept.in_(condition.get('dept')))
	if condition.get('account'):
		if isinstance(condition.get('account'), str):
			result = result.filter(UserModel.account == condition.get('account'))
		if isinstance(condition.get('account'), list):
			result = result.filter(UserModel.account.in_(condition.get('account')))
	if condition.get('realname'):
		if isinstance(condition.get('realname'), str):
			result = result.filter(UserModel.realname == condition.get('realname'))
		if isinstance(condition.get('realname'), list):
			result = result.filter(UserModel.realname.in_(condition.get('realname')))
	if result:
		return [(res.realname, res.email) for res in result]


if __name__ == "__main__":
	print(get_user_email({'dept': 5, 'account': ['hmc', 'gjh']}))
	print(get_user_email({'dept': 5, 'account': [], 'realname': '费鑫'}))
