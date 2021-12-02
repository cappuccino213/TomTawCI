"""
@File : tools_router.py
@Date : 2021/12/1 14:28
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""
# 常用工具的调用

from fastapi import APIRouter
from app.schemas import tools_schemas
from app.utils import compress
from app.utils.response_code import *

router = APIRouter(prefix="/ewordci/tools", tags=["tools"])


@router.post("/package", name="文件打包成*.7z")
def package(package_param: tools_schemas.Package):
	try:
		compress.compress_to_7z(package_param.src_dir_path, package_param.dst_file_path, package_param.password)
		return resp_200(dict(), message="已将文件打包至{}".format(package_param.dst_file_path))
	except Exception as e:
		return resp_400(message="打包失败，原因{}".str(e))


@router.post("/mail", name="邮件通知")
async def mail():
	return "自动发布"


if __name__ == "__main__":
	pass
