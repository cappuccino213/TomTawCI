"""
@File : dev_task_router.py
@Date : 2022/6/24 11:37
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""
from fastapi import APIRouter

from app.db.database import engine, Base
from app.schemas import dev_task_schemas
from app.models import dev_task_model
from app.utils import response_code

Base.metadata.create_all(bind=engine)

router = APIRouter(prefix="/ewordci/devtask", tags=["devtask"])


@router.post("/query", name="查询任务列表")
async def query_build(param: dev_task_schemas.DevTaskList):
	dev_task_list = dev_task_model.query_dev_task_list(param.dict())
	if dev_task_list:
		return response_code.resp_200(dev_task_list)
	else:
		return response_code.resp_404(message="找不到任务信息")


if __name__ == "__main__":
	pass
