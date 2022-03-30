"""
@File : CI_server_router.py
@Date : 2022/3/30 15:03
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""
from fastapi import APIRouter
from app.utils import response_code

router = APIRouter(prefix="/ewordci/ci_server", tags=["ci_server"])


# 检测API是否启动
@router.get("/check", name="检测API服务是否正常启动")
async def check():
	return response_code.resp_200("WelCome to eWordCI", message="Success")


if __name__ == "__main__":
	pass
