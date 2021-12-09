"""
@File : team_router.py
@Date : 2021/12/1 14:44
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""
from fastapi import APIRouter
from app.models.team_model import *
from app.utils import response_code

router = APIRouter(prefix="/ewordci/team", tags=["team"])


@router.get("/get-by-project", name="根据项目id获取团队信息")
async def get_team_by_project(project_id: int):
	team = query_by_project(project_id)
	if team:
		return response_code.resp_200(team)
	else:
		return response_code.resp_404(message="找不到项目id={}的团队数据".format(project_id))


# 处理获取的团队成员信息按role分组
# def sort_by_role(team_infos: list[dict]):
# 	sort_list = list()
# 	for team_info in team_infos:
# 		print(team_info.get('role'))


@router.get("/get-sortby-role", name="项目id获取团队信息,按照角色分组")
async def get_team_sort_by_role(project_id: int):
	team = get_team_info(project_id)
	if team:
		return response_code.resp_200(team)
	else:
		return response_code.resp_404(message="找不到项目id={}的团队数据".format(project_id))


if __name__ == "__main__":
	# sort_by_role(get_team_info(66))
	pass