"""
@File : tools_schemas.py
@Date : 2021/12/2 16:10
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""
# 关于工具的schema
from pydantic import BaseModel, EmailStr, validator
from enum import Enum
from typing import Optional, List


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
	release_manual = 'release_manual'  # 发布单手动填写发布人员


# 邮件通知入参
class EmailNotice(BaseModel):
	notice_type: EmailType
	business_id: int
	server_account: EmailStr
	server_password: str
	email_to: Optional[List[str]]

	# 参数校验，当notice_type的值未release_manual时，需要传email_to
	# @validator('email_to')
	# def email_to_rule(cls):
	# 	if 'notice_type' == 'release_manual':
	# 		if not 'email_to':
	# 			raise ValueError("'when notice_type is release_manual,email_to must be a list,like ['zyp','zhangl']'")
	# 		else:
	# 			return True


if __name__ == "__main__":
	pass
	en = EmailNotice(notice_type='release_manual', business_id=1, server_account='1661886732@qq.com',
					 server_password='xxx',
					 # email_to=[('方敏芳', '1661886732@qq.com'), ('钱迁', '360309531@qq.com')])
					 email_to=['zyp', 'fmf'])
	print(en.json())
