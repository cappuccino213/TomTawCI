"""
@File : database1.py
@Date : 2021/10/9 15:08
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import DATABASE_CONFIGURE
from app.utils.custom_log import *

# 创建SQLAlchemy的engine
engine = create_engine(DATABASE_CONFIGURE["SQLALCHEMY_DATABASE_URL"], echo=DATABASE_CONFIGURE["SQL_ECHO"],
					   pool_pre_ping=True, pool_recycle=3600)  # 解决Mysql Server has gone away的问题
# poolclass=NullPool)  # 如果想要在调用conn.close()时，真正的关闭连接，可以使用poolclass=NullPool属性

# 创建SessionLocal类,每个实例都是一个数据库的会话
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Session = SessionLocal()

# Base是用来给model类继承的
Base = declarative_base()


# 查询
def get_list(primary_id: int, models: Base):
	"""
	根据表的主键id查询
	:param primary_id: 主键id
	:param models: 继承Base的对象
	:return: 返回类型是list
	"""
	try:
		return Session.query(models).filter(models.id == primary_id).all()
	except Exception as e:
		logging.error(str(e))
	finally:
		Session.close()


def get(primary_id: int, models: Base):
	"""
	根据表的主键id查询
	:param primary_id: 主键id
	:param models: 继承Base的对象
	:return:
	"""
	try:
		return Session.query(models).filter(models.id == primary_id).first()
	except Exception as e:
		logging.error(str(e))
	finally:
		Session.close()


# 新增
def create(db_model):
	"""
	:param db_model: db的model对象的实例
	:return:
	"""
	try:
		Session.add(db_model)
		Session.commit()
		Session.refresh(db_model)  # 为了读取自增字段(如果有的话)到对象
		Session.expunge(db_model)
	except Exception as e:
		logging.error(str(e))
		Session.rollback()
		Session.flush()
	finally:
		Session.close()


# 批量新增
def create_all(db_model_list):
	"""
	可以批量insert数据
	:param db_model_list: list(db_model)
	:return:
	"""
	try:
		Session.add_all(db_model_list)
		Session.commit()
		for db_model in db_model_list:
			Session.refresh(db_model)
			Session.expunge(db_model)
	except Exception as e:
		logging.error(str(e))
		Session.rollback()
		Session.flush()
	finally:
		Session.close()


# 更新
def update(schema, models: Base):
	"""
	先用入参json中的id查找记录，然后修改信息
	:param schema:
	:param models:
	:return:
	"""
	update_column = get(schema.id, models)
	get_column = update_column.to_dict()
	if update_column:  # 判断被修改的数据是否存在
		update_dict = schema.dict()  # 将查询到的列记录转成dict类型
		try:  # 使用遍历k,v方式对应赋值
			for k, v in update_dict.items():
				if get_column.get(k) != v:  # 判断是传入的值与原始值是否一样，不一样则更新
					Session.query(models).filter(models.id == schema.id).update({k: v})
			Session.commit()  # 提交修改
			Session.flush()
			return update_column
		except Exception as e:
			logging.error(str(e))
			Session.rollback()
			Session.flush()
		finally:
			Session.close()


# 删除
def remove(primary_id, models: Base):
	remove_column = get(primary_id, models)
	if remove_column:
		try:
			# setattr(remove_column, 'deleted', '1')
			Session.query(models).filter(models.id == primary_id).update({'deleted': '1'})
			Session.commit()
			Session.flush()
			# Session.refresh(remove_column)
			return remove_column
		except Exception as e:
			logging.error(str(e))
			Session.rollback()
			Session.flush()
		finally:
			Session.close()


# 执行sql语句,返回list[dict]
def execute_sql(statement):
	try:
		cur_res = Session.execute(statement)
		res_list = cur_res.all()
		return [(res._mapping) for res in res_list]  # 返回字典项
	except Exception as e:
		logging.error(str(e))
	finally:
		Session.close()


if __name__ == "__main__":
	from app.models import build_model
	# from app.models import release_model
	from datetime import datetime
	from app.schemas.build_schemas import Build

	d = {'id': 643, 'name': '1.0.1.4', 'branch': 0, 'product': 21, 'project': 62,
		 'scmPath': r'\\192.168.1.19\delivery\eWordERS\1.0.1.36.20211230',
		 'filePath': r'\\192.168.1.19\delivery\eWordERS\1.0.1.36.20211230', 'date': '2021-12-30', 'stories': '',
		 'bugs': '', 'builder': 'wangj1', 'desc': 'ceshi1', 'deleted': '0'}
	b = Build(**d)
	update(b, build_model.BuildModel)
# print(get(673, build_model.BuildModel).to_dict())
