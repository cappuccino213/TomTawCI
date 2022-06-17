"""
@File : compress.py
@Date : 2021/11/29 15:55
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""
import datetime

import py7zr
import os

from app.utils.excute_shell import *


def compress_to_7z(src_dir, dst_path, password):
	"""
	将文件夹压缩成7z的格式(空文件夹不会压缩)
	:param src_dir: 压缩源文件目录
	:param dst_path: 压缩目的.7z文件路径
	:param password: 压缩加密码
	:return:
	"""

	# 判断是否安装了bandizip(一款免费的高效压缩工具)
	if "Bandizip console tool" in run_shell("bz"):
		compress_cli = f'bz c -p:{password} "{dst_path}" "{src_dir}"'
		logging.info(f"启用Bandizip进行压缩")
		run_shell(compress_cli)

	# 否则用7z库压缩
	else:
		logging.info("建议安装高效压缩工具Bandizip，访问地址:https://cn.bandisoft.com/bandizip/")
		logging.info("未检测到Bandizip，故使用py7zr库进行压缩，请等待......")
		folder_path = os.path.abspath(src_dir)  # 取压缩源目录绝对路径
		if not os.path.exists(folder_path):
			os.makedirs(folder_path)
		with py7zr.SevenZipFile(dst_path, mode='w', password=password) as zf:
			zf.set_encrypted_header(True)
			for dir_path, dir_names, file_names in os.walk(src_dir):
				for file_name in file_names:
					f_path = dir_path.replace(src_dir, '')
					file_path = os.path.join(dir_path, file_name)
					file_name = os.path.join(f_path, file_name)
					zf.write(file_path, arcname=file_name)


if __name__ == "__main__":
	pass
	src_dir1 = r"\\192.168.1.19\delivery\eWordRIS\V2.2.2.44834466690000.20220614"
	dst_dir1 = r"D:\CI_Client\temp\V2.2.2.44834466690000.20220614.7z"

	start = datetime.datetime.now()
	compress_to_7z(src_dir1, dst_dir1, 'TomTaw@HZ')
	# multi_thread_compress_to_7z(src_dir1, dst_dir1, 'TomTaw@HZ')
	print(datetime.datetime.now() - start)
