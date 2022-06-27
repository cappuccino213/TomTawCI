"""
@File : bug_schemas.py
@Date : 2022/6/24 10:09
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""

from pydantic import BaseModel
from typing import Optional


class BugList(BaseModel):
	project: Optional[int]
	status: Optional[str]
	resolvedBuild: Optional[int]

	class Config:
		schema_extra = {
			"example": {
				"project": 35,
				"status": "resolved",
				"resolvedBuild": 864
			}
		}


if __name__ == "__main__":
	pass
