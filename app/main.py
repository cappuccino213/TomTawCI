"""
@File : main.py
@Date : 2021/10/9 14:41
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""
from fastapi import FastAPI
from routers import (test_report_router,
					 bug_related_evaluations_router,
					 test_task_router)
from starlette.responses import RedirectResponse
import uvicorn

app = FastAPI()

# 注册路由
app.include_router(test_report_router.router)
app.include_router(bug_related_evaluations_router.router)
app.include_router(test_task_router.router)


@app.get("/")
# 将根路径重定向到swagger文档
async def root():
	# return {"message": "Welcome to eWordCI"}
	return RedirectResponse(url="/docs/")


if __name__ == "__main__":
	uvicorn.run(app='main:app', host="0.0.0.0", port=8889, reload=True, debug=True)
