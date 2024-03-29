"""
@File : business_auto_distribute.py
@Date : 2021/11/29 16:41
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""
import datetime

from fastapi import APIRouter
from app.schemas import release_schemas
from app.config import ROOT_DIRECTORY
from app.utils import html2string, response_code, reporlab_pdf,file_handle
from datetime import date
from app.models.release_model import ReleaseModel
from app.models.build_model import query_build_multiple_condition
from app.models.action_model import *
from app.db.database import *
from app.config import AUTO_DISTRIBUTE
import os

RELEASE_TEMPLATE_PATH = os.path.join(ROOT_DIRECTORY, 'static', AUTO_DISTRIBUTE['TEMPLATE'])

router = APIRouter(prefix="/ewordci/auto-distribute", tags=["business"])


# 从入参取出发布单的入库dict
def get_release_dict_from_param(param: release_schemas.CreateRelease):
    param_dict = param.dict()

    # 相关人员获取，由于禅道权限划分的特殊性，需要特殊处理
    dev_member = ','.join(
        [member['name'] for member in param_dict['members'] if member['role'] in ['研发', '研发主管']])
    qa_member = ','.join([member['name'] for member in param_dict['members'] if '测试' in member['role']])
    pm_member = ','.join(
        [member['name'] for member in param_dict['members'] if
         (member['role'] == '研发主管' and member['name'] != '胡东慧')])

    # 发布描述处理

    desc_dict = dict(releaseBuild='{0}.{1}.b{2}'.format(param_dict['build_name'], param_dict['release_type'],
                                                        str(date.today()).replace('-', '')),
                     applyScope=param_dict['apply_scope'],
                     releaseContent=param_dict['release_content'],
                     changelogUrl=param_dict['ChangeLog_url'],
                     updateNote=param_dict['update_note'],
                     attention=param_dict['attention'],
                     releaseLink=param_dict['release_link'],
                     # members=param_dict['members'],
                     devMember=dev_member,
                     qaMember=qa_member,
                     PMMember=pm_member,
                     releaser=param_dict['releaser'],
                     compress_pwd=param_dict['compress_secret'])

    # 描述转化成html
    desc = html2string.release_html2string(RELEASE_TEMPLATE_PATH, desc_dict)
    # 增加一个PMMember返回字段，发布审核单要用到，将返回值改成tuple
    return dict(product=param_dict['product'], build=param_dict['build'],
                name=f"{param_dict['product_code']} {desc_dict['releaseBuild']}",
                marker=param_dict['marker'],
                date=date.today(), desc=desc),desc_dict['PMMember']


@router.post("/create", name="自动发布版本-创建发布单")
async def auto_distribute(release_info: release_schemas.CreateRelease):
    release_data = get_release_dict_from_param(release_info)
    release_dict = release_data[0]
    db_release = ReleaseModel(release_dict)
    # 创建发布单
    create(db_release)

    # 插入操作日志
    db_action = ActionModel(
        get_action_dict('release', db_release.id, db_release.product, release_info.project,
                        release_info.releaser, 'opened'))
    create(db_action)

    # 获取递交路径、打包路径，作为返参用
    build_param = dict(name=release_info.build_name, product=release_info.product, project=release_info.project)
    src_dir_path = query_build_multiple_condition(build_param)[0].filePath  # 如果获取到结果为空这里就会报错
    dst_file_path = os.path.join(AUTO_DISTRIBUTE['COMPRESS_PATH'],
                                 release_info.product_code,
                                 str(datetime.datetime.now().year),  # 增加一级当下的年份路径
                                 f"{release_dict['name']}.7z")
    compress_info = dict(src_dir_path=src_dir_path, dst_file_path=dst_file_path)

    # 判断是否存在打包目录，如不存在就要创建
    compress_folder = os.path.split(dst_file_path)[0]
    if not os.path.exists(compress_folder):
        print(f"打包目录{compress_folder}不存在,即将被创建...")
        os.mkdir(compress_folder)

    # 生成发布审批单
    today_date = datetime.datetime.now().date()

    # 创建发布单文件夹
    approval_form_dir = os.path.join(os.path.split(dst_file_path)[0],'ApprovalForm')
    file_handle.make_dir(approval_form_dir)

    approval_form_dict = dict(product_name=release_info.product_name,
                              product_code=release_info.product_code,
                              build_name=release_info.build_name,
                              project_begin=(today_date-datetime.timedelta(days=3)).strftime("%Y年%m月%d日"),# 取三天前的日期
                              project_end=today_date.strftime("%Y年%m月%d日"),
                              approval_form_path=os.path.join(approval_form_dir,f"{release_dict['name']}发布审批单.pdf"),
                              qa_name = release_info.releaser, # 测试人员
                              pm_name = release_data[1] # 开发人员
                              )
    reporlab_pdf.generate_release_approval_form(**approval_form_dict)

    if db_release.id:  # 根据有没有生成新的id判断是否插入成功
        # return response_code.resp_200({'release': db_release.to_dict(), 'compress_info': compress_info})
        return response_code.resp_200({'release': db_release.id, 'compress_info': compress_info})  # 返回发布单id
    else:
        return response_code.resp_400(message="发布单创建失败")


@router.post("/upload", name="自动发布版本-程序入版本仓库")
async def auto_base(release_info: release_schemas.CreateRelease):
    return "自动入仓库"


if __name__ == "__main__":
    eg = {
        "product": 7,
        "product_name": "产品名称",
        "build": 642,
        "build_name": "V2.2.0.4286(版本名称)",
        "release_type": "发布类型（M:里程碑版本，RTX：正式版本，RC：预发布版本，Beta：测试发布版本）",
        "marker": "0(0,1是否为里程碑版本)",
        "date": "yyyy-mm-dd（发布日期可选，默认为当天）",
        "apply_scope": "适用范围（通用、OEM）",
        "release_content": "发布内容",
        "ChangeLog_url": "changlog的链接",
        "update_note": "更新说明的链接",
        "attention": "注意事项，html格式",
        "release_link": "发布链接，html格式",
        "members": "相关人员，html格式",
        "releaser": "发布人员（当前登录人员）"
    }
    print(get_release_dict_from_param(release_schemas.CreateRelease(**eg)))
