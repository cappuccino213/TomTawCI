"""
@File : compress.py
@Date : 2021/11/29 15:55
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""

import py7zr
import os


def compress_to_7z(src_dir, dst_path, password):
	"""
	将文件夹压缩成7z的格式(空文件夹不会压缩)
	:param src_dir: 压缩源文件目录
	:param dst_path: 压缩目的.7z文件路径
	:param password: 压缩加密码
	:return:
	"""
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
	# src_dir1 = r"C:\Users\eword\Desktop\V2.2.0.4306.20211126"
	src_dir1 = r"\\192.168.1.19\delivery\全网云通用浏览器\V1.1.0.409"
	# dst_dir1 = r"C:\Users\eword\Desktop\eWordRIS V2.2.0.4306.RTX.b20211126.7"
	dst_dir1 = r"\\192.168.1.19\distribution\全网云通用浏览器\V1.1.0.409.M.b20211209.7z"
	compress_to_7z(src_dir1, dst_dir1, 'TomTaw@HZ')
