"""
@File : projectstory_model.py
@Date : 2023/6/25 16:24
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""
"""项目需求表"""

from sqlalchemy import Column, Integer, SmallInteger, Enum, DateTime, desc

from app.db.database import Base, Session

from app.utils.custom_log import *

"""需求"""


class ProjectStoryModel(Base):
    __tablename__ = "zt_projectstory"

    project = Column(Integer)  # 所属产品id
    product = Column(Integer,primary_key=True)  # 所属项目id
    story = Column(Integer,primary_key=True)  # 需求ID
    version = Column(SmallInteger)  # 版本
    order = Column(SmallInteger)  # 序号

    def to_dict(self):  # 用将数据列转换成dict
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


    # 多条件查询
    @classmethod
    def query_project_story(cls,condition: dict):
        try:
            result = Session.query(cls)
            if condition.get('product'):
                result = result.filter(cls.product == condition.get('product'))
            if condition.get('project'):
                result = result.filter(cls.project == condition.get('project'))
            if condition.get('story'):
                result = result.filter(cls.story == condition.get('story'))
            if condition.get('version'):
                result = result.filter(cls.version == condition.get('version'))
            if condition.get('order'):
                result = result.filter(cls.order == condition.get('order'))
            return result.first()
        except Exception as e:
            logging.error(str(e))
        finally:
            Session.close()


if __name__ == "__main__":
    logging.info(ProjectStoryModel().query_project_story(dict(product=7,story=740)).to_dict())
