"""
@File : projectstory_router.py
@Date : 2023/6/25 16:52
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""
from fastapi import APIRouter
from app.models.projectstory_model import ProjectStoryModel
from app.utils import response_code
from app.schemas import story_schemas
from app.db.database import engine, Base

Base.metadata.create_all(bind=engine)

router = APIRouter(prefix="/ewordci/projectstory", tags=["projectstory"])


@router.post("/info", name="查询项目需求信息")
async def query_project_story_info(query_condition: story_schemas.QueryProjectStory):
    project_story_info = ProjectStoryModel.query_project_story(query_condition.dict())
    if project_story_info:
        return response_code.resp_200(project_story_info)
    else:
        return response_code.resp_400(message="暂无数据")


if __name__ == "__main__":
    pass
