"""
@File : z_mail.py
@Date : 2021/12/7 16:15
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""
import zmail


def z_mail(mail_struct: dict[str], mail_server: dict[str], mail_to: [list, str], mail_cc: list[tuple, str]):
	"""
	通过zmail库发送邮件，参考地址
	https://github.com/zhangyunhao116/zmail/blob/master/README-cn.md
	:param mail_struct: 邮件结构 {'subject':'主题',
								'from':'发送人'，例如'from':'Boss <mymail@foo.com>',
								'content_text':'邮件文本内容'，
								'content_html':'邮件html内容',
								'attachments':'邮件附件'例如 '/User/apple/1.txt' or ['/User/apple/1.txt','2.txt'] or [('1.txt',b'...'),('2.txt',b'...')] )}
	:param mail_server:邮件服务器{'account':邮件地址,'password':邮件密码}
	:param mail_to:发送地址'yourfriend@example.com'或者['yourfriend1@example.com','yourfriend2@example.com']
	:param mail_cc:抄送地址[('Boss','bar@163.com'),'bar@126.com']也可以为他们命名(使用元组，第一个为其命名，第二个为其地址)
	:return:
	"""
	server = zmail.server(mail_server['account'], mail_server['password'])
	server.send_mail(mail_to, mail_struct, cc=mail_cc)


if __name__ == "__main__":
	test_mail = {
		'from': '张烨平 <1483029082@qq.com>',
		'subject': '【eWordRIS V2.2.0.4306.RTX.b20211209】发布告知_By Zmail',
		'content_html': """
		<table class="table table-kindeditor" style="width:1146px;color:#3C4353;">
	  <tbody>
	    <tr>
	      <td>发布版本号<br /></td>
	      <td>V2.2.0.4306.RTX.b20211126<br /></td>
	    </tr>
	    <tr>
	      <td>测试版本号</td>
	      <td>V2.2.0.4300、V2.2.0.4306</td>
	    </tr>
	    <tr>
	      <td>适用范围</td>
	      <td>通用</td>
	    </tr>
	    <tr>
	      <td>发布内容</td>
	      <td>RIS程序包</td>
	    </tr>
	    <tr>
	      <td>ChangeLog</td>
	      <td><a href="https://www.yuque.com/docs/share/5bd14755-4ab0-4c83-a66a-9171d9154c88?" target="_blank">https://www.yuque.com/docs/share/5bd14755-4ab0-4c83-a66a-9171d9154c88?</a>#（密码：kut1） 《eWordRIS ChangeLogs》<br /></td>
	    </tr>
	    <tr>
	      <td>更新说明</td>
	      <td>https://www.yuque.com/docs/share/14d6b2bf-bc2f-46a2-9f88-354608b90e7e?#（密码：eqi7） 《eWordRIS 更新说明》<br /></td>
	    </tr>
	    <tr>
	      <td>注意事项</td>
	      <td>
	        <p>更新内容：<span style="background-color:#E53333;">请详见ChangeLog</span></p>
	        <p>新安装注意事项：</p>
	        <ul style="margin-left:0px;">
	          <li>1部署文档：https://www.yuque.com/docs/share/0ca79f11-eee0-4928-b9a4-18339f54f98d?#（密码：di20） 《RIS部署文档》</li>
	          <li>
	            <p class="MsoNormal">2打印模板配置字段对照说明：<a href="https://docs.qq.com/doc/DSmtjVHVpZnpzdFl4" target="_blank">https://docs.qq.com/doc/DSmtjVHVpZnpzdFl4</a></p>
	          </li>
	          <li>
	            <p class="MsoNormal">3发布版本命名说明：<a href="/zentao/doc-view-49.html" target="_blank">http://eword.66ip.net:8086/zentao/doc-view-49.html</a></p>
	          </li>
	        </ul>
	        <p>升级注意事项：</p>
	        <ul>
	          <li>推荐使用配置文件更新法</li>
	          <li>将原配置文件appsettings.json、DBConfig.json、log4net.config，复制到更新包中，然后重命名为原程序文件名</li>
	          <li>其中appsettings.json的版本后缀建议修改成"VersionSuffix": ".RTX<span>.b20211126</span>"<br /></li>
	          <li>备份旧程序文件名，以日期的格式</li>
	        </ul>
	      </td>
	    </tr>
	    <tr>
	      <td>发布链接</td>
	      <td>
	        <p class="MsoNormal" style="margin-left:0pt;">1登录悦库，链接：<a href="http://eword.66ip.net:2020/index.html" target="_blank">http://eword.66ip.net:2020/index.html</a>，账号：ime&nbsp; 密码：TomTaw@HZ</p>
	        <p class="MsoNormal" style="margin-left:0pt;">2到相应的路径下，下载对应的发布版本</p>
	        <p class="MsoNormal" style="margin-left:0pt;">RIS路径：公共空间&gt;版本库&gt;eWordRIS&gt;通用版本</p>
	        <p class="MsoNormal" style="margin-left:0pt;">3程序包解压密码：TomTaw@HZ</p>
	      </td>
	    </tr>
	    <tr>
	      <td>相关人员</td>
	      <td>
	        <p class="MsoNormal">研发人员：王晶、李鹏龙、欧进、胡东慧 &nbsp;&nbsp;</p>
	        <p class="MsoNormal">测试人员：张烨平</p>
	        <p class="MsoNormal">产品经理：王晶</p>
	      </td>
	    </tr>
	    <tr>
	      <td>发布人</td>
	      <td>张烨平</td>
	    </tr>
	  </tbody>
	</table>
		"""
	}
	test_server = dict(account='1483029082@qq.com', password='lqmfvhxhzotdidjb')
	test_to = ['526856808@qq.com', '303140237@qq.com']
	test_cc = [('zyp', '1483029082@qq.com')]
	z_mail(test_mail, test_server, test_to, test_cc)
