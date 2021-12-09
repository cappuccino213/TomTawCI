"""
@File : html2string.py
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


# 测试报告模板
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


# 测试单模板
def task_html2string(html_file, desc: dict):
	with open(html_file, 'r', encoding="utf-8") as f:
		html_str = f.read().format(ifSmoke=desc.get('ifSmoke'), manTime=desc.get('manTime'),
								   testType=desc.get('testType'),
								   testSuggest=desc.get('testSuggest'), buildDesc=desc.get('buildDesc'))

	return html_str


# 发布单模板
def release_html2string(html_file, desc: dict):
	"""
	根据描述的信息，按照制定的html模板生成发布描述的html字符串信息
	:param desc_info:
	:return: html的str
	"""
	with open(html_file, 'r', encoding="utf-8") as f:
		html_str = f.read().format(releaseBuild=desc.get('releaseBuild'),
								   applyScope=desc.get('applyScope'),
								   releaseContent=desc.get('releaseContent'),
								   changelogUrl=desc.get('changelogUrl'),
								   updateNote=desc.get('updateNote'),
								   attention=desc.get('attention'),
								   releaseLink=desc.get('releaseLink'),
								   # members=desc.get('members'),
								   devMember=desc.get('devMember'),
								   qaMember=desc.get('qaMember'),
								   PMMember=desc.get('PMMember'),
								   releaser=desc.get('releaser'))
	return html_str


if __name__ == "__main__":
	hf = r'D:\Python\Project\pythonProject\TomTawCI\app\static\reportSummary.html'
	s = dict(testTime="1MD", testURL="http://192.168.1.18:8141",
			 testClient="Win10Pro Core(TM) i5-7500 CPU 16G RAM",
			 testTools="DevTools")
	report_html2string(hf, s)
