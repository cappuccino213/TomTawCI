"""
@File : main.py
@Date : 2021/10/9 14:41
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""

from fastapi import FastAPI
from app.routers import (
	user_router, test_report_router,
	build_router,
	bug_related_evaluations_router,
	test_task_router,
	team_router,
	business_auto_deliver_test,
	business_auto_create_report,
	business_product_project,
	business_auto_distribute,
	tools_router)
from starlette.responses import RedirectResponse
from app.config import RUN_CONFIGURE
import uvicorn

app = FastAPI()

"""注册路由"""
# 基础数据
app.include_router(user_router.router)
app.include_router(build_router.router)
app.include_router(test_task_router.router)
app.include_router(test_report_router.router)
app.include_router(team_router.router)

# 业务
app.include_router(bug_related_evaluations_router.router)
app.include_router(business_auto_create_report.router)
app.include_router(business_product_project.router)
app.include_router(business_auto_deliver_test.router)
app.include_router(business_auto_distribute.router)

# 工具
app.include_router(tools_router.router)


@app.get("/", name="WelCome to fastapi!!!")
# 将根路径重定向到swagger文档
async def root():
	# return {"message": "Welcome to eWordCI"}
	return RedirectResponse(url="/docs")


if __name__ == "__main__":
	# 脚本启动
	uvicorn.run(app='main:app', host="0.0.0.0", port=RUN_CONFIGURE['PORT'], reload=RUN_CONFIGURE['RELOAD'],
				debug=RUN_CONFIGURE['DEBUG'], workers=RUN_CONFIGURE['WORKERS'])
# uvicorn.run(app='main:app', host="0.0.0.0", port=8889, reload=True, debug=False, workers=4)

# 命令行启动
# 部署到linux可以使用gunicorn框架做监控 https://www.jianshu.com/p/c292e2f79c2c
# uvicorn main:app --host 0.0.0.0 --port 8889 --reload
