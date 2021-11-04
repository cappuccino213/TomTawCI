"""
@File : html_handler.py
@Date : 2021/11/3 16:48
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""
from html.parser import HTMLParser
import os

class CIHTMLParser(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.data = []

	# 覆写starttag方法
	def handle_starttag(self, tag, attrs):
		pass

	# 覆写endtag方法
	def handle_endtag(self, tag):
		pass

	# 覆写handler_data方法
	def handle_data(self, data):
		if data.count('\n') == 0:
			self.data.append(data)


def html_content(html_file):
	with open(html_file, 'r') as html_file:
		content = html_file.read()
		parser = CIHTMLParser()
		parser.feed(content)
		return parser.data


if __name__ == "__main__":
	print(html_content(r'D:\Python\Project\pythonProject\TomTawCI\app\static\reportSummary.html'))
