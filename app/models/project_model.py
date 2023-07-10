"""
@File : project_model.py
@Date : 2023/6/30 14:01
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""
from sqlalchemy import Column, Integer, String, Date, SmallInteger, DateTime

from app.db.database import Base, Session
from app.utils.custom_log import logging

"""为RDM系统查询用的project的视图"""
class ProjectModel(Base):
    __tablename__ = "rdm_project"

    id = Column(Integer, primary_key=True)
    type = Column(String(20))
    name = Column(String(90))
    code = Column(String(45)) # 项目编码
    begin = Column(Date)
    end = Column(Date)
    days = Column(SmallInteger)  # 工期
    status = Column(String(10))  # 状态
    Leader = Column(String(30))  # 项目经理
    createUser = Column(String(30))  # 创建人
    createDate = Column(DateTime)  # 创建日期
    product = Column(Integer)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

    @classmethod
    def query_project_list(cls, condition: dict):
        try:
            result = Session.query(cls)
            if condition.get('type'):
                result = result.filter(cls.type == condition.get('type'))
            if condition.get('code'):
                result = result.filter(cls.code == condition.get('code'))
            if condition.get('status'):
                result = result.filter(cls.status == condition.get('status'))
            if condition.get('Leader'):
                result = result.filter(cls.Leader == condition.get('Leader'))
            if condition.get('createUser'):
                result = result.filter(cls.createUser == condition.get('createUser'))
            if condition.get('product'):
                result = result.filter(cls.product == condition.get('product'))
            if condition.get('begin'):
                # 以结束日期查询
                result = result.filter(cls.begin >= condition.get('begin'))
            if condition.get('end'):
                result = result.filter(cls.end <= condition.get('end'))
            return result.all()
        except Exception as e:
            logging.error(str(e))
        finally:
            Session.close()


if __name__ == "__main__":
    pass
