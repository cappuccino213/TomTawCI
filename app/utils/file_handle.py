"""
@File : file_handle.py
@Date : 2021/12/29 13:53
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""
# 复制文件到指定目录
import shutil

import os

from app.utils.custom_log import logging


def copy_file(src_file, dst_dir):
	shutil.copy(src_file, dst_dir)
	logging.info("copy file:【{}】 to 【{}】 finished".format(src_file, dst_dir))


# 创建文件夹
def make_dir(folder_path):
	if not os.path.exists(folder_path):
		os.mkdir(folder_path)

if __name__ == "__main__":
	pass
	# copy_file(r'\\192.168.1.19\delivery\eWordRIS\V2.2.0.4231.20211022.zip',r'Y:\公共空间\temp\瑞康需求')
	# copy_file(r'C:\Users\eword\Desktop\eWordRIS-20211111160400.zip',r'Y:\公共空间\temp')

	make_dir(r'\\192.168.1.19\delivery\temp\2025')

	# os.mkdir(r'\\192.168.1.19\distribution\eWordDEP\2023\1')