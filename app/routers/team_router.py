"""
@File : team_router.py
@Date : 2021/12/1 14:44
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""
from fastapi import APIRouter
from app.models.team_models import *
from app.utils import response_code

router = APIRouter(prefix="/ewordci/team", tags=["team"])


# @router.post("/getlist", name="团队列表")
# async def get_team_list():
# 	pass


@router.get("/get-by-project", name="根据项目id获取团队信息")
async def get_team_by_project(project_id: int):
	team = query_by_project(project_id)
	if team:
		return response_code.resp_200(team)
	else:
		return response_code.resp_404(message="找不到项目id={}的团队数据".format(project_id))


if __name__ == "__main__":
	pass
