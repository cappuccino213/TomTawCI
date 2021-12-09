"""
@File : user_router.py
@Date : 2021/11/23 16:43
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""
from app.db.database import *
from fastapi import APIRouter
from app.models.user_model import *
from app.utils import response_code
from app.schemas import user_schemas

Base.metadata.create_all(bind=engine)

# 获取研发用户
# def get_rds():
# 	return query_by_dept('3')


router = APIRouter(prefix="/ewordci/user", tags=["user"])


@router.get("/rd_users/get", name="获取研发用户")
async def get_rds_list():
	rds_list = query_by_dept('3')
	if rds_list:
		return response_code.resp_200(rds_list)
	else:
		return response_code.resp_404(message="无研发用户".format(rds_list))


@router.get("/qa_users/get", name="获取测试用户")
async def get_qas_list():
	rds_list = query_by_dept('4')
	if rds_list:
		return response_code.resp_200(rds_list)
	else:
		return response_code.resp_404(message="无测试用户".format(rds_list))


@router.post("/user_list/get", name="获取用户列表")
async def get_qas_list(user_condition: user_schemas.User):
	rds_list = query_multiple_condition(user_condition.dict())
	if rds_list:
		return response_code.resp_200(rds_list)
	else:
		return response_code.resp_404(message="查无用户".format(rds_list))


if __name__ == "__main__":
	pass
