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
from app.utils.log import *

# 创建SQLAlchemy的engine
engine = create_engine(DATABASE_CONFIGURE["SQLALCHEMY_DATABASE_URL"], echo=DATABASE_CONFIGURE["SQL_ECHO"],
					   pool_pre_ping=True)

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
	logging.info('获取成功')
	return Session.query(models).filter(models.id == primary_id).all()


def get(primary_id: int, models: Base):
	"""
	根据表的主键id查询
	:param primary_id: 主键id
	:param models: 继承Base的对象
	:return:
	"""
	return Session.query(models).filter(models.id == primary_id).first()


# 新增
def create(schema):
	"""
	:param schema: schemas定义的类
	:return:
	"""
	try:
		Session.add(schema)
		Session.commit()
		Session.refresh(schema)
	except Exception as e:
		print(str(e))
		Session.rollback()
		Session.flush()


# 批量新增
def create_all(schemas):
	"""
	可以批量insert数据
	:param schemas: list(schema)
	:return:
	"""
	try:
		Session.add_all(schemas)
		Session.commit()
		Session.refresh(schemas)
	except Exception as e:
		print(str(e))
		Session.rollback()
		Session.flush()


# 更新
def update(schema, models: Base):
	"""
	先用入参json中的id查找记录，然后修改信息
	:param schema:
	:param models:
	:return:
	"""
	update_column = get(schema.id, models)
	if update_column:  # 判断被修改的数据是否存在
		update_dict = schema.dict()  # 将查询到的列记录转成dict类型
		try:  # 使用遍历k,v方式对应赋值
			for k, v in update_dict.items():
				setattr(update_column, k, v)  # setattr给对象的属性赋值 https://www.runoob.com/python/python-func-setattr.html
			Session.commit()  # 提交修改
			Session.flush()
			Session.refresh(update_column)
			return update_column
		except Exception as e:
			print(str(e))
			Session.rollback()
			Session.flush()


# 删除
def remove(primary_id, models: Base):
	remove_column = get(primary_id, models)
	if remove_column:
		try:
			setattr(remove_column, 'deleted', '1')
			Session.commit()
			Session.flush()
			Session.refresh(remove_column)
			return remove_column
		except Exception as e:
			print(str(e))
			Session.rollback()
			Session.flush()


# 执行sql语句,返回list[dict]
def execute_sql(statement):
	cur_res = Session.execute(statement)
	res_list = cur_res.all()
	# return res_list  # 返回字典项
	return [(res._mapping) for res in res_list]  # 返回字典项


if __name__ == "__main__":
	sql = """SELECT
	product AS product_id,
	pd.`name` AS product_name,
	project AS project_id,
	pj.`name` AS project_name 
FROM
	zt_projectproduct pp
	LEFT JOIN zt_product pd ON pp.product = pd.id
	LEFT JOIN zt_project pj ON pp.project = pj.id 
WHERE
	pd.deleted = '0' 
	AND pj.deleted = '0'"""

	# res_list = execute_sql(sql)
	# [print(i._mapping) for i in res_list]
	# print(execute_sql(sql))
	from app.models import release_model
	print(get(237,release_model.ReleaseModel))