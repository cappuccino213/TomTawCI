"""
@File : project_router.py
@Date : 2023/6/30 15:22
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""
from fastapi import APIRouter

from app.schemas import project_schemas

from app.models.project_model import ProjectModel

from app.utils import response_code

router = APIRouter(prefix="/ewordci/project", tags=["project"])


@router.post("/list", name="查询项目列表")
async def query_story_list(query_condition: project_schemas.QueryProject):
    project_list = ProjectModel.query_project_list(query_condition.dict())
    if project_list:
        return response_code.resp_200(project_list)
    else:
        return response_code.resp_400(message="暂无数据")



if __name__ == "__main__":
    pass
