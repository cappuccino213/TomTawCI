"""
@File : test_report_model.py
@Date : 2021/10/9 14:42
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from app.db.database import  engine
# from app.schemas import test_report_schemas
from app.models.test_report_model import *
from app.utils import response_code

Base.metadata.create_all(bind=engine)

# 路由的参数有prefix、tags、responses等，详见https://fastapi.tiangolo.com/zh/tutorial/bigger-applications/
router = APIRouter(prefix="/ewordci/testreport", tags=["testreport"])  # 路由前缀,tags给接口分组


@router.get("/get", name="获取测试报告信息")
async def get_test_report(report_id: int):
	report_list = get(report_id)
	res_list = []
	if report_list:
		for report_dict in report_list:
			res_list.append(report_dict.to_dict())

		return response_code.resp_200(report_list)
	else:
		return response_code.resp_404(message="找不到id={}的测试报告".format(report_id))


@router.post("/create", response_model=test_report_schemas.TestReport, name="创建测试报告")
async def test_report_create(report: test_report_schemas.TestReport):
	report_json = jsonable_encoder(report)  # 将入参json格式化
	db_test_report = TestReportModels(report_json)  # 入参传入数据模型
	create(db_test_report)  # 调用新增数据库方法
	if db_test_report.id:  # 根据有没有生成新的id判断是否插入成功
		return response_code.resp_200(db_test_report.to_dict())
	else:
		return response_code.resp_400(message="报告新增失败")


@router.put("/update", response_model=test_report_schemas.TestReport, name="修改测试报告")
async def test_report_update(report: test_report_schemas.TestReport):
	if_success = update(report)
	if if_success:
		return response_code.resp_200(report.dict(), massage="修改测试报告成功")
	else:
		return response_code.resp_404(message="修改id={}的测试报告失败".format(report.id))


@router.delete("/delete", name="删除测试报告")
async def test_report_del(report_id: int):
	if_success = remove(report_id)
	if if_success:
		return response_code.resp_200([if_success.to_dict()], massage="删除测试报告成功")
	else:
		return response_code.resp_404(message="删除id={}的测试报告失败".format(report_id))


if __name__ == "__main__":
	pass
