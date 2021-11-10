"""
@File : generate_report_summary_html.py
@Date : 2021/11/3 16:48
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""
# 用于生成测试总结的html的字符串

"""
解析 html
from html.parser import HTMLParser
# 参考文档 https://docs.python.org/zh-cn/3/library/html.parser.html

class CIHTMLParser(HTMLParser):
	# def __init__(self):
	# 	HTMLParser.__init__(self)
	# 	self.data = []

	# 覆写starttag方法
	def handle_starttag(self, tag, attrs):
		print("start tag:", tag)

	# 覆写endtag方法
	def handle_endtag(self, tag):
		print("end tag :", tag)

	# 覆写handler_data方法
	def handle_data(self, data):
		print("Data     :", data)

def html_content(html_file):
	with open(html_file, 'r', encoding="utf-8") as file:
		content = file.read()
		parser = CIHTMLParser()
		parser.feed(content)  # 填充一些文本到解析器中
		return parser
"""


def report_html2string(html_file, summary: dict):
	with open(html_file, 'r', encoding="utf-8") as f:
		# 将值填入报告的变量值，使用get方法取字典值，防止取不到值的抛异常
		html_str = f.read().format(build=summary.get('build'), testTime=summary.get('testTime'),
								   testURL=summary.get('testURL'),
								   testClient=summary.get('testClient'), testTools=summary.get('testTools'),
								   testTask=summary.get('testTask'), riskEvaluation=summary.get('riskEvaluation'),
								   summary=summary.get('summary'), instabilityValue=summary.get('instabilityValue'),
								   quality=summary.get('quality'), if_release=summary.get('if_release'))
	# print(html_str)
	return html_str


# return html_str


if __name__ == "__main__":
	hf = r'D:\Python\Project\pythonProject\TomTawCI\app\static\reportSummary.html'
	s = dict(testTime="1MD", testURL="http://192.168.1.18:8141",
				   testClient="Win10Pro Core(TM) i5-7500 CPU 16G RAM",
				   testTools="DevTools")
	report_html2string(hf, s)
