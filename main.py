"""
@File : main.py
@Date : 2021/10/9 14:41
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""

from fastapi import FastAPI
from app.routers import (
    user_router, test_report_router,
    build_router, bug_router, dev_task_router,
    bug_related_evaluations_router,
    test_task_router,
    projectstory_router,
    team_router,
    story_router,
    project_router,
    business_auto_deliver_test,
    business_auto_create_report,
    business_product_project,
    business_auto_distribute,
    tools_router,
    CD_server_router,
    CI_server_router)
from starlette.responses import RedirectResponse
from app.config import RUN_CONFIGURE
from app.utils.log_handle import *
from app.config import LOG_CONFIG
from pathlib import Path
import uvicorn
import sys
import os


# 引入日志模块
def init_app():
    application = FastAPI(title="eWordCIAPI 全网云CI系统", debug=LOG_CONFIG['IF_DEBUG'])
    logging.getLogger().handlers = [InterceptHandler()]
    logger.configure(
        handlers=[{"sink": sys.stdout, "level": logging.DEBUG, "format": format_record}])
    logger.add(LOG_CONFIG['LOG_PATH'], rotation=LOG_CONFIG['ROTATION'], encoding="utf-8", enqueue=True,
               retention=LOG_CONFIG['RETENTION'])
    logger.debug('日志系统已加载')
    logging.getLogger("uvicorn.access").handlers = [InterceptHandler()]
    return application


# 初始化app
app = init_app()

# app = FastAPI()

"""注册路由到app"""
# 基础数据
app.include_router(user_router.router)
app.include_router(build_router.router)
app.include_router(test_task_router.router)
app.include_router(test_report_router.router)
app.include_router(team_router.router)
app.include_router(bug_router.router)
app.include_router(dev_task_router.router)
app.include_router(story_router.router)
app.include_router(projectstory_router.router)
app.include_router(project_router.router)

# 业务
app.include_router(bug_related_evaluations_router.router)
app.include_router(business_auto_create_report.router)
app.include_router(business_product_project.router)
app.include_router(business_auto_deliver_test.router)
app.include_router(business_auto_distribute.router)

# 工具
app.include_router(tools_router.router)

# CD服务端
app.include_router(CD_server_router.router)

# CI
app.include_router(CI_server_router.router)


@app.get("/", name="WelCome to CIAPI!")
# 将根路径重定向到swagger文档
async def root():
    # return {"message": "Welcome to eWordCI"}
    return RedirectResponse(url="/docs")


if __name__ == "__main__":
    root_path = Path(__file__).parent  # 获取当前文件的父路径
    os.chdir(root_path)  # 切换程序运行目录
    # 脚本启动
    uvicorn.run(app='main:app', host="0.0.0.0", port=RUN_CONFIGURE['PORT'], reload=RUN_CONFIGURE['RELOAD'],
                debug=RUN_CONFIGURE['DEBUG'], workers=RUN_CONFIGURE['WORKERS'])

"""
命令行启动
部署到linux可以使用gunicorn框架做监控 https://www.jianshu.com/p/c292e2f79c2c
uvicorn main:app --host 0.0.0.0 --port 8889 --reload
"""
