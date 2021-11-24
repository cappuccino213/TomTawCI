"""
@File : test_task_router.py
@Date : 2021/11/1 18:02
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""
from app.db.database import *
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from app.models.test_task_model import TestTaskModel
from app.utils import response_code
from app.schemas import test_task_schemas

Base.metadata.create_all(bind=engine)

# 路由的参数有prefix、tags、responses等，详见https://fastapi.tiangolo.com/zh/tutorial/bigger-applications/
router = APIRouter(prefix="/ewordci/testtask", tags=["testtask"])  # 路由前缀,tags给接口分组


@router.get("/get", name="获取测试单信息")
async def get_test_task(task_id: int):
	test_task = get(task_id, TestTaskModel)
	if test_task:
		res_list = [test_task.to_dict()]
		return response_code.resp_200(res_list)
	else:
		return response_code.resp_404(message="找不到id={}的测试单".format(task_id))


@router.post("/create", response_model=test_task_schemas.TestTask, name="创建测试单")
async def test_task_create(test_task: test_task_schemas.TestTask):
	task_json = jsonable_encoder(test_task)  # 将入参json格式化
	db_test_task = TestTaskModel(task_json)  # 入参传入数据模型
	create(db_test_task)  # 调用新增数据库方法
	if db_test_task.id:  # 根据有没有生成新的id判断是否插入成功
		return response_code.resp_200(db_test_task.to_dict())
	else:
		return response_code.resp_400(message="测试单新增失败")


if __name__ == "__main__":
	pass
