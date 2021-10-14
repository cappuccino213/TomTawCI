"""
@File : bug_model.py
@Date : 2021/10/12 16:06
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""

"""bug相关的评估函数"""


# 不稳定系数（instability）IN值计算
def calculate_in_value(severity: dict[str:int]):
	# fatal: int, severe: int, mistake: int, suggest: int
	return severity['fatal'] * 30 + severity['severe'] * 15 + severity['mistake'] * 5 + severity['suggest'] * 1


# 提测质量评估，根据in值计算
def evaluate_grade(in_value: int):
	if in_value >= 30:
		return '不合格'
	elif in_value >= 15:
		return '合格'
	elif in_value >= 10:
		return '良好'
	else:
		return '优秀'


# 版本发布评估
def release_evaluation(in_value: int):
	if in_value < 15:
		return '允许发布'
	else:
		return '不予发布'


if __name__ == "__main__":
	bug_num = {'fatal': 0, 'severe': 1, 'mistake': 2, 'suggest': 3}
	ins_value = calculate_in_value(bug_num)
	print(ins_value)
	print(evaluate_grade(ins_value))
	print(release_evaluation(ins_value))
