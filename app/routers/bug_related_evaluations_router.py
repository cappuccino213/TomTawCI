"""
@File : bug_related_evaluations_router.py
@Date : 2021/10/12 16:29
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""
from fastapi import APIRouter
from app.db.database import engine, Base
from app.schemas import bug_related_schemas
from app.models import bug_model
from app.utils import response_code

Base.metadata.create_all(bind=engine)

router = APIRouter(prefix="/ewordci/bug-related", tags=["bug-related"])


@router.post("/build-evaluation", name="通过bug等级数量评估提测质量", response_model=bug_related_schemas.BuildQualityEvaluation)
async def get_build_quality(bug_severity_num: bug_related_schemas.BugSeverityNum):
	in_value = bug_model.calculate_in_value(bug_severity_num.dict())
	grade = bug_model.evaluate_grade(in_value)
	release = bug_model.release_evaluation(in_value)
	bqe = bug_related_schemas.BuildQualityEvaluation(IN_value=in_value, evaluate_grade=grade,
													 release_evaluation=release)
	if bqe:
		return response_code.resp_200(bqe.dict())
	else:
		return response_code.resp_404(message="计算失败")


@router.get("/build-evaluation-by-task_id", name="通过测试单获取提测质量",
			response_model=bug_related_schemas.BuildQualityEvaluation)
async def get_build_quality(task_id: int):
	in_value = bug_model.calculate_in_value(bug_model.get_testtask_bug_statistics(task_id))
	grade = bug_model.evaluate_grade(in_value)
	release = bug_model.release_evaluation(in_value)
	bqe = bug_related_schemas.BuildQualityEvaluation(IN_value=in_value, evaluate_grade=grade,
													 release_evaluation=release)
	if bqe:
		return response_code.resp_200(bqe.dict())
	else:
		return response_code.resp_404(message="计算失败")


if __name__ == "__main__":
	pass
