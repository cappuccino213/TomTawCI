"""
@File : html2string.py
@Date : 2021/11/3 16:48
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""
import re
from bs4 import BeautifulSoup

# 用于生成测试总结的html的字符串



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
								   releaser=desc.get('releaser'),
								   compressPwd=desc.get('compress_pwd'))
	return html_str


# 将html转化成纯文本
def convert_html_to_text(input_str):
	"""
	智能转换HTML到纯文本，自动处理：
	- 标签大小写（如<BR>、<Div>）
	- 空标签过滤
	- 智能换行逻辑
	"""
	if not input_str:
		return input_str

	# 统一用BeautifulSoup规范化HTML标签（自动转小写）
	soup = BeautifulSoup(input_str, 'html.parser')

	# 处理所有换行相关标签（兼容任意大小写写法）
	for tag in ['br', 'p', 'div']:  # 已统一按小写处理
		for elem in soup.find_all(tag):
			elem.append('\n')  # 插入换行符

	# 获取处理后的纯文本
	text = soup.get_text(separator='\n',strip=True)

	# 优化换行格式：保留段落间距，合并多余空行
	return re.sub(r'\n{3,}', '\n\n', re.sub(r'[\r\n]+', '\n', text)).strip()


if __name__ == "__main__":
	# hf = r'D:\Python\Project\pythonProject\TomTawCI\app\static\reportSummary.html'
	# s = dict(testTime="1MD", testURL="http://192.168.1.18:8141",
	# 		 testClient="Win10Pro Core(TM) i5-7500 CPU 16G RAM",
	# 		 testTools="DevTools")
	# report_html2string(hf, s)
	test_html = convert_html_to_text("""<p>完成docker镜像发布的完成流程功能<br />1.打包镜像-从harbor上下载镜像，打包成tar包存放本地image_tar目录，镜像地址支持从禅道的版本id获取<br />2.生成docker-compose.yml<br />3.程序版本打包（tar+yml--&gt;7z）<br />4.发布程序版本<br />5.清除发布源文件<br />6.清除打包文件</p>
<p>&nbsp;</p>""")

	# 将转化后的文本写入到txt
	with open(r'D:\Python\Project\pythonProject\TomTawCI\tests\test.txt', 'w', encoding='utf-8') as f:
		f.write(convert_html_to_text(test_html))
