"""
@File : story_router.py
@Date : 2023/6/14 16:50
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""
from fastapi import APIRouter

from app.schemas import story_schemas

from app.models.story_model import StoryModel

from app.utils import response_code

router = APIRouter(prefix="/ewordci/story", tags=["story"])


@router.post("/list", name="查询需求列表")
async def query_story_list(query_condition: story_schemas.QueryStory):
    story_list = StoryModel.query_story_list(query_condition.dict())
    if story_list:
        return response_code.resp_200(story_list)
    else:
        return response_code.resp_400(message="暂无数据")


if __name__ == "__main__":
    pass
