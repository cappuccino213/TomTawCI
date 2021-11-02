"""
@File : test_task_router.py
@Date : 2021/11/1 18:02
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""

from fastapi import APIRouter
from app.db.database import engine
from app.models.test_task_model import *
from app.utils import response_code

Base.metadata.create_all(bind=engine)

# 路由的参数有prefix、tags、responses等，详见https://fastapi.tiangolo.com/zh/tutorial/bigger-applications/
router = APIRouter(prefix="/ewordci/testtask", tags=["testtask"])  # 路由前缀,tags给接口分组


@router.get("/get", name="获取测试单信息")
async def get_test_report(task_id: int):
	test_task = get_by_id(task_id)
	if test_task:
		res_list = [test_task.to_dict()]
		return response_code.resp_200(res_list)
	else:
		return response_code.resp_404(message="找不到id={}的测试报告".format(task_id))

if __name__ == "__main__":
	pass
