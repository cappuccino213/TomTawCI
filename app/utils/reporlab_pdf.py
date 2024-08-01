"""
@File : reporlab_pdf.py
@Date : 2023/10/11 10:38
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""
import os
from pathlib import Path

# 用于生成pdf报告

from reportlab.lib.units import cm, inch  # 单位
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont  # 字体
from reportlab.lib.styles import getSampleStyleSheet  # 样式
from reportlab.platypus import Paragraph, SimpleDocTemplate, Table  # 模板、表格
from reportlab.platypus.flowables import Image  # 图片

from reportlab.lib.pagesizes import A4  # 页面尺寸
from reportlab.lib import colors  # 颜色模块
from app.config import ROOT_DIRECTORY, AUTO_DISTRIBUTE

font_path = os.path.join(ROOT_DIRECTORY, 'static', AUTO_DISTRIBUTE['FONT_PATH'])
sign_image = os.path.join(ROOT_DIRECTORY, 'utils', 'sign_img')

# 注册字体
pdfmetrics.registerFont(TTFont('SimSun', font_path))

class Graph:

    # 标题
    @staticmethod
    def draw_title(title: str):
        # 获取样式
        style = getSampleStyleSheet()
        # 获取标题样式
        ts = style['Heading1']
        # 设置相关属性
        ts.fontName = 'SimSun'
        ts.fontSize = 20
        ts.leading = 50
        ts.alignment = 1  # 居中

        # 填入标题字符
        return Paragraph(title, ts)

    # 生成手写签名的图片
    @staticmethod
    def signature_image(name: str):
        gif_file = f'{name}.gif'
        # image = Image(r'.\sign_img\{0}.gif'.format(name))
        image = Image(Path(sign_image,gif_file))
        # image.drawHeight = 2 * cm * Img.drawHeight / Img.drawWidth
        image.drawHeight = 1 * inch * image.drawHeight / image.drawWidth
        # image.drawWidth = 4 * cm
        image.drawWidth = 1.25 * inch
        return image

    # 绘制发布单表格
    @staticmethod
    def draw_table(*args):
        # 设置列宽度
        # col_width = 120
        # 设置行高
        # line_height = 30

        # 设置表格样式
        style = [
            # 字体设置
            ('FONTNAME', (0, 0), (-1, -1), 'SimSun'),  # 字体
            ('FONTSIZE', (0, 0), (-1, -1), 12),  # 设置标题字体大小
            # 设置内容字体大小
            ('FONTSIZE', (1, 0), (1, 0), 10.5),
            ('FONTSIZE', (3, 0), (3, 0), 10.5),
            ('FONTSIZE', (1, 1), (1, 1), 10.5),
            ('FONTSIZE', (3, 1), (3, 1), 10.5),
            ('FONTSIZE', (1, 2), (1, 2), 10.5),
            ('FONTSIZE', (3, 2), (3, 2), 10.5),
            ('FONTSIZE', (0, 3), (-1, -1), 11),

            # 对齐方式
            # 标题居左对齐
            # ('ALIGN', (0, 0), (0, 0), 'LEFT'),

            # 内容居中对齐
            ('ALIGN', (1, 0), (1, 0), 'CENTER'),
            ('ALIGN', (3, 0), (3, 0), 'CENTER'),
            ('ALIGN', (1, 1), (1, 1), 'CENTER'),
            ('ALIGN', (3, 1), (3, 1), 'CENTER'),
            ('ALIGN', (1, 2), (1, 2), 'CENTER'),
            ('ALIGN', (3, 2), (3, 2), 'CENTER'),

            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # 垂直居中对齐
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),  # 边框颜色
            ('INNERGRID', (0, 3), (0, 3), 0.5, colors.transparent),  # 边框颜色

            # 表格合并
            ('SPAN', (0, 3), (-1, 3)),  # 合并列
            ('SPAN', (0, 4), (-1, 4)),
            ('SPAN', (0, 5), (-1, 5)),
            ('SPAN', (0, 6), (-1, 6)),
            ('SPAN', (0, 7), (-1, 7)),
            ('SPAN', (0, 8), (-1, 8)),
            ('SPAN', (0, 9), (-1, 9)),
            ('SPAN', (1, 10), (-1, 10)),
            ('SPAN', (0, 11), (-1, 11)),
            ('SPAN', (1, 12), (-1, 12))
        ]
        # table = Table(args, colWidths=col_width, rowHeights=None, style=style)
        table = Table(args, colWidths=[3 * cm, 5.5 * cm, 3 * cm, 5.5 * cm], rowHeights=None, style=style)
        return table


# 生成发布审核单pdf
def generate_release_approval_form(**kwargs):
    # 表格内容
    content = list()

    # 填写标题
    content.append(Graph.draw_title('软件产品发布审批表'))

    # 定义表格数据
    table_data = [
        ('产品名称', kwargs['product_name'], '试产数量', '1'),
        ('规格型号', kwargs['product_code'], '起始日期', kwargs['project_begin']),
        ('版本号', kwargs['build_name'], '总结日期', kwargs['project_end']),
        ('一、试产前期工作：', '', '', ''),
        (
            '  在各项检测、检验以及其他操作人员均接受过相应主管部门的培训，并经考核合格后上岗。\n公司测试人员（张烨平、张林）、场地等准备工作到位后，于{0}起动该项目。'.format(
                kwargs['project_begin'].split('月')[0]+'月'),
            '', '', ''),
        ('二、产品检验、试验结果简介及其结论', '', '', ''),
        ('  各阶段按要求均通过检测。', '', '', ''),
        ('三、试产结论及建议', '', '', ''),
        ('  通过各项功能均通过检测。', '', '', ''),
        ('四、审核意见', '', '', ''),
        ('通过', [Graph.signature_image(kwargs['qa_name']), Graph.signature_image(kwargs['pm_name'])], ''),
        ('五、主管领导批示', '', '', ''),
        ('通过', Graph.signature_image('黄燕平'),)
    ]
    content.append(Graph.draw_table(*table_data))

    # 生成pdf文件
    pdf = SimpleDocTemplate(kwargs['approval_form_path'], pagesize=A4)
    pdf.build(content)
    print(f"生成审批单成功，路径：{kwargs['approval_form_path']}")


if __name__ == "__main__":
    pass
