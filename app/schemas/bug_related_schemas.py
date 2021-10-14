"""
@File : bug_related_schemas.py
@Date : 2021/10/13 9:35
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""

from pydantic import BaseModel
# from typing import Optional


# bug等级数量分布
class BugSeverityNum(BaseModel):
	# 致命，严重，错误，一般
	fatal: int = 0
	severe: int = 0
	mistake: int = 0
	suggest: int = 0


# 根据bug相关的提测版本质量的评估
class BuildQualityEvaluation(BaseModel):
	IN_value: int
	evaluate_grade: str
	release_evaluation: str


if __name__ == "__main__":
	be = BuildQualityEvaluation(IN_value=15, evaluate_grade='合格', release_evaluation='允许发布')
	print(be.json())
