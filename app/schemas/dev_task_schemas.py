"""
@File : dev_task_schemas.py
@Date : 2022/6/24 11:34
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""
from pydantic import BaseModel
from typing import Optional


class DevTaskList(BaseModel):
	project: Optional[int]
	status: Optional[str]
	assignedTo: Optional[str]
	timeRange: Optional[int]

	class Config:
		schema_extra = {
			"example": {
				"project": 35,
				"status": "done",
				"assignedTo": "hyp",
				"timeRange": 7
			}
		}


if __name__ == "__main__":
	pass
