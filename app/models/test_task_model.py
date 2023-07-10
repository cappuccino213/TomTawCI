"""
@File : test_task_model.py
@Date : 2021/11/2 9:30
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""
from app.db.database import Base
from sqlalchemy import Column, String, Integer, Date, Enum, Text
from app.db.database import Session
from datetime import date
from app.utils.custom_log import *


class TestTaskModel(Base):
    __tablename__ = "zt_testtask"

    id = Column(Integer, primary_key=True)
    name = Column(String(90))
    product = Column(Integer)
    project = Column(Integer)
    build = Column(String(30))
    owner = Column(String(30))
    pri = Column(Integer, default=2)
    begin = Column(Date, default=date.today())
    end = Column(Date, default=date.today())
    mailto = Column(Text)

    desc = Column(Text)
    report = Column(Text, default='CI系统自动生成')  # 数据库中为非空字段给个默认值
    auto = Column(String(10), default='no')
    subStatus = Column(String(30), default='NA')
    status = Column(Enum('blocked', 'doing', 'wait', 'done'), default='wait')
    deleted = Column(Enum('0', '1'), default='0')

    def __init__(self, fields_dict: dict):
        self.id = fields_dict.get('id')
        self.name = fields_dict.get('name')
        self.product = fields_dict.get('product')
        self.project = fields_dict.get('project')
        self.build = fields_dict.get('build')
        self.owner = fields_dict.get('owner')
        self.pri = fields_dict.get('pri')
        self.begin = fields_dict.get('begin')
        self.end = fields_dict.get('end')
        self.mailto = fields_dict.get('mailto')
        self.desc = fields_dict.get('desc')
        self.status = fields_dict.get('status')
        self.deleted = fields_dict.get('deleted')

    # 用将数据列转换成dict
    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


# 未写测试报告的测试单
class TestTaskWithoutReport(Base):
    __tablename__ = "zt_testtask_without_report"

    id = Column(Integer, primary_key=True)
    name = Column(String(90))
    product = Column(Integer)
    project = Column(Integer)
    build = Column(String(30))
    owner = Column(String(30))
    begin = Column(Date, default=date.today())
    end = Column(Date, default=date.today())
    desc = Column(Text)

    # 用将数据列转换成dict
    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


"""TestTaskModel相关的函数"""


# 通过测试单号获取版本详情
def get_build_details(task_id):
    try:
        cur_res = Session.execute(
            'SELECT * FROM zt_build WHERE id in (SELECT build FROM zt_testtask WHERE id = :id)', {'id': task_id})
        res_list = cur_res.first()
        return res_list._mapping  # 返回字典项
    except Exception as e:
        logging.error(str(e))
    finally:
        Session.close()


# 单条件查询测试单
def query_testtask(condition: dict):
    try:
        result = Session.query(TestTaskModel)
        if condition.get('id'):
            result = result.filter(TestTaskModel.id == condition.get('id'))
        if condition.get('product'):
            result = result.filter(TestTaskModel.product == condition.get('product'))
        if condition.get('project'):
            result = result.filter(TestTaskModel.project == condition.get('project'))
        if condition.get('owner'):
            result = result.filter(TestTaskModel.owner == condition.get('owner'))
        if condition.get('build'):
            result = result.filter(TestTaskModel.build == condition.get('build'))
        return result.filter(TestTaskModel.deleted == '0').first()
    except Exception as e:
        logging.error(str(e))
    finally:
        Session.close()


# 多条件查询测试单
def query_test_task_list(condition: dict):


    try:
        result = Session.query(TestTaskModel)
        if condition.get('product'):
            result = result.filter(TestTaskModel.product == condition.get('product'))
        if condition.get('project'):
            result = result.filter(TestTaskModel.project == condition.get('project'))
        if condition.get('owner'):
            result = result.filter(TestTaskModel.owner == condition.get('owner'))
        if condition.get('build'):
            result = result.filter(TestTaskModel.build == condition.get('build'))
        # 只获取进行中和完成的任务
        if condition.get('status') in ('doing','done'):
            result = result.filter(TestTaskModel.status == condition.get('status'))
        if condition.get('begin'):
            # 以结束日期查询
            result = result.filter(TestTaskModel.end >= condition.get('begin'))
        if condition.get('end'):
            result = result.filter(TestTaskModel.end <= condition.get('end'))
        return result.filter(TestTaskModel.deleted == '0').all()
    except Exception as e:
        logging.error(str(e))
    finally:
        Session.close()


"""TestTaskWithoutReport"""


# 单条件查询
def query_task_single_condition(condition: dict):
    try:
        result = Session.query(TestTaskWithoutReport)
        if condition.get('id') != 0:
            result = result.filter(TestTaskWithoutReport.id == condition.get('id'))
        if condition.get('product') != 0:
            result = result.filter(TestTaskWithoutReport.product == condition.get('product'))
        if condition.get('project') != 0:
            result = result.filter(TestTaskWithoutReport.project == condition.get('project'))
        if condition.get('owner') != '':
            result = result.filter(TestTaskWithoutReport.owner == condition.get('owner'))
        if condition.get('build') != '':
            result = result.filter(TestTaskWithoutReport.build == condition.get('build'))
        return result.all()
    except Exception as e:
        logging.error(str(e))
    finally:
        Session.close()


# 多条件查询
def query_task_multiple_condition(condition: dict):
    try:
        result = Session.query(TestTaskWithoutReport)
        if len(condition.get('id')):
            result = result.filter(TestTaskWithoutReport.id.in_(condition.get('id')))
        if len(condition.get('product')):
            result = result.filter(TestTaskWithoutReport.product.in_(condition.get('product')))
        if len(condition.get('project')):
            result = result.filter(TestTaskWithoutReport.project.in_(condition.get('project')))
        if condition.get('owner'):
            result = result.filter(TestTaskWithoutReport.owner == (condition.get('owner')))
        return result.all()
    except Exception as e:
        logging.error(str(e))
    finally:
        Session.close()


if __name__ == "__main__":
    # print(get_by_id(245).to_dict().get('status'))
    # print(get_build_details(643))
    # print(query_multiple_condition({'id':666}))
    c = {
        "id": [666],
        "product": [0],
        "project": [0],
        "owner": ""
    }
    # print(query_multiple_condition(c)[0].to_dict())

    d = dict(build=677)
    print(query_testtask(d).id)
