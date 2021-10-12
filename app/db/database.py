"""
@File : database1.py
@Date : 2021/10/9 15:08
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from ..config import *

# 创建SQLAlchemy的engine
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True, pool_pre_ping=True)

# 创建SessionLocal类,每个实例都是一个数据库的会话
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Session = SessionLocal()

# Base是用来给model类继承的
Base = declarative_base()

if __name__ == "__main__":
	pass
