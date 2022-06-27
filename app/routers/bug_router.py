"""
@File : bug_router.py
@Date : 2022/6/24 10:06
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""

from fastapi import APIRouter

from app.db.database import engine, Base
from app.schemas import bug_schemas
from app.models import bug_model
from app.utils import response_code

Base.metadata.create_all(bind=engine)

router = APIRouter(prefix="/ewordci/bug", tags=["bug"])


@router.post("/query", name="查询缺陷列表")
async def query_build(param: bug_schemas.BugList):
	bug_list = bug_model.query_bug_list(param.dict())
	if bug_list:
		return response_code.resp_200(bug_list)
	else:
		return response_code.resp_404(message="找不到bug信息")


if __name__ == "__main__":
	pass
