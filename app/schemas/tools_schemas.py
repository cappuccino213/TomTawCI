"""
@File : tools_schemas.py
@Date : 2021/12/2 16:10
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""
# 关于工具的schema
from pydantic import BaseModel, EmailStr
from enum import Enum


# 打包入参，将文件包压缩放到指定的位置
# class Package(BaseModel):
# 	src_dir_path: DirectoryPath
# 	dst_file_path: FilePath
# 	password: Optional[str] = 'TomTaw@HZ'
#
# 	class Config:
# 		schema_extra = {
# 			"example": {
# 				"src_dir_path": r"\\192.168.1.19\delivery\eWordRIS\V2.2.0.4316.20211202",
# 				"dst_file_path": r"\\192.168.1.19\distribution\eWordRIS\V2.2.0.4316.20211202.7z",
# 				"password": "TomTaw@HZ"
# 			}
# 		}
# 邮件通知类型
class EmailType(str, Enum):
	test_task = 'test_task'
	test_report = 'test_report'
	release = 'release'


# 邮件通知入参
class EmailNotice(BaseModel):
	notice_type: EmailType
	business_id: int
	server_account: EmailStr
	server_password: str


if __name__ == "__main__":
	pass
