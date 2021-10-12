"""
@File : response_code.py
@Date : 2021/9/17 16:22
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""
from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, Response
from typing import Union


# 响应状态的封装
# 其他状态处理可见https://github.com/CoderCharm/FastAdmin/blob/master/backend/app/api/utils/response_code.py
def resp_200(data: Union[list, dict, str], massage="Success") -> Response:
	return JSONResponse(
		status_code=status.HTTP_200_OK,
		content={'code': 200,
				 'message': massage,
				 'data': jsonable_encoder(data)  # models类型转换成json对象才能放到JSONResponse中
				 }
	)


def resp_204(data: str = None, message: str = "No Content") -> Response:
	return JSONResponse(
		status_code=status.HTTP_400_BAD_REQUEST,
		content={'code': 204,
				 'message': message,
				 'data': jsonable_encoder(data)
				 }
	)


def resp_400(data: str = None, message: str = "BAD REQUEST") -> Response:
	return JSONResponse(
		status_code=status.HTTP_400_BAD_REQUEST,
		content={'code': 400,
				 'message': message,
				 'data': jsonable_encoder(data)
				 }
	)


def resp_404(data: str = None, message: str = "NOT FOUND") -> Response:
	return JSONResponse(
		status_code=status.HTTP_404_NOT_FOUND,
		content={'code': 404,
				 'message': message,
				 'data': jsonable_encoder(data)
				 }
	)


if __name__ == "__main__":
	pass
