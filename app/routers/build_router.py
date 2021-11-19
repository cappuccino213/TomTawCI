"""
@File : build_router.py
@Date : 2021/11/19 14:34
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""
from app.db.database import *
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from app.models.build_model import BuildModel
from app.utils import response_code
from app.schemas import build_schemas

Base.metadata.create_all(bind=engine)

router = APIRouter(prefix="/ewordci/build", tags=["build"])


@router.get("/get", name="获取版本信息")
async def get_build_info(build_id: int):
	build_info = get_list(build_id, BuildModel)
	if build_info:
		return response_code.resp_200(build_info)
	else:
		return response_code.resp_404(message="找不到id={}的版本信息".format(build_id))


@router.post("/create", response_model=build_schemas.Build, name="创建版本")
async def build_create(build: build_schemas.Build):
	build_json = jsonable_encoder(build)
	build_db = BuildModel(build_json)
	create(build_db)
	if build_db.id:
		return response_code.resp_200(build_db.to_dict())
	else:
		return response_code.resp_400(message="创建版本失败")


if __name__ == "__main__":
	pass
