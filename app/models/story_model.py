"""
@File : story_model.py
@Date : 2023/6/14 15:18
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""
from sqlalchemy import Column, Integer, String, Enum, DateTime, desc

from app.db.database import Base, Session

from app.utils.custom_log import *

"""需求"""


class StoryModel(Base):
    __tablename__ = "zt_story"

    id = Column(Integer, autoincrement=True, primary_key=True)
    product = Column(Integer)  # 所属产品id
    title = Column(String(255))  # 需求名称
    type = Column(String(30))  # 需求类型
    pri = Column(Integer)  # 优先级
    status = Column(Enum('', 'changed', 'active', 'draft', 'closed'))  # 当前状态
    stage = Column(
        Enum('', 'wait', 'planned', 'projected', 'developing', 'developed', 'testing', 'tested', 'verified',
             'released', 'closed'))  # 所处阶段
    # openedBy = Column(String(30))  # 创建人
    # openedDate = Column(DateTime)
    # assignedTo = Column(String(30))  # 责任人
    # assignedDate = Column(DateTime)
    # reviewedBy = Column(String(30))  # 评审者
    # reviewedDate = Column(DateTime)
    version = Column(Integer)  # 版本号
    # closedBy = Column(String(30))
    # closedDate = Column(DateTime)  # 关闭日期
    lastEditedBy = Column(String(30))
    lastEditedDate = Column(DateTime)
    deleted = Column(Enum('0', '1'))

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

    # 多条件查询需求列表
    @classmethod
    def query_story_list(cls, condition: dict):
        try:
            result = Session.query(cls).filter(cls.deleted == '0')
            if condition.get('product'):
                result = result.filter(cls.product == condition.get('product'))
            if condition.get('status'):
                result = result.filter(cls.status == condition.get('status'))
            if condition.get('owner'):
                result = result.filter(cls.lastEditedBy == condition.get('owner'))
            if condition.get('begin'):
                # 以结束日期查询
                result = result.filter(cls.lastEditedDate >= condition.get('begin'))
            if condition.get('end'):
                result = result.filter(cls.lastEditedDate <= condition.get('end'))
            return result.order_by(desc(cls.id)).all()
        except Exception as e:
            logging.error(str(e))
        finally:
            Session.close()


if __name__ == "__main__":
    pass
