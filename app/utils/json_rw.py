"""
@File : json_rw.py
@Date : 2022/1/24 14:54
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""
from app.utils.custom_log import logging
from pathlib import Path
import json
import os

# 为了避免引入此模块时改变了相对路径导致读取文件失败的问题
os.chdir(Path(__file__).parent)


# 将数据写入json文件
def write_json(content: list[dict], json_file='../static/CDClientInfo.json'):
	try:
		with open(json_file, 'w', encoding='utf-8') as f:
			json.dump(content, f, ensure_ascii=False)
			logging.info("写入文件{0}成功\n内容为：{1}".format(json_file, content))
			return content
	except Exception as e:
		logging.error(str(e))


# 读取指定的json文件
def read_json(json_file='../static/CDClientInfo.json'):
	try:
		with open(json_file, 'r', encoding='utf-8') as load_f:
			load_dict = json.load(load_f)
			logging.info("读取文件{0}成功\n内容为：{1}".format(json_file, load_dict))
			return load_dict
	except Exception as e:
		logging.error(str(e))


if __name__ == "__main__":
	# read_json('CDClientInfo.json')
	# write_json('../static/CDClientInfo.json', [{'hostname': 'DESKTOP-L7R9KAB', 'ip': '192.168.1.56', 'desc': '本地测试机1'}])
	print(read_json())
	print(type(read_json()))
