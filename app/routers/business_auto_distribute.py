"""
@File : business_auto_distribute.py
@Date : 2021/11/29 16:41
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""
from fastapi import APIRouter
from app.schemas import release_schemas
from app.config import ROOT_DIRECTORY, AUTO_DISTRIBUTE
from app.utils import html2string, response_code
from datetime import date
from app.models.release_models import ReleaseModel
from app.db.database import *
import os

RELEASE_TEMPLATE_PATH = os.path.join(ROOT_DIRECTORY, 'static', AUTO_DISTRIBUTE['TEMPLATE'])

router = APIRouter(prefix="/ewordci/auto-distribute", tags=["business"])


# 从入参取出发布单的入库dict
def get_release_dict_from_param(param: release_schemas.CreateRelease):
	param_dict = param.dict()
	desc_dict = dict(releaseBuild='{}.{}.b{}'.format(param_dict['build_name'], param_dict['release_type'],
													 str(date.today()).replace('-', '')),
					 applyScope=param_dict['apply_scope'],
					 releaseContent=param_dict['release_content'],
					 changelogUrl=param_dict['ChangeLog_url'],
					 updateNote=param_dict['update_note'],
					 attention=param_dict['attention'],
					 releaseLink=param_dict['release_link'],
					 members=param_dict['members'],
					 releaser=param_dict['releaser'])
	desc = html2string.release_html2string(RELEASE_TEMPLATE_PATH, desc_dict)
	return dict(product=param_dict['product'], build=param_dict['build'],
				name='{} {}'.format(param_dict['product_name'], desc_dict['releaseBuild']), marker=param_dict['marker'],
				date=date.today(), desc=desc)


@router.post("/create", name="自动发布版本-创建发布单")
async def auto_distribute(release_info: release_schemas.CreateRelease):
	release_dict = get_release_dict_from_param(release_info)
	db_release = ReleaseModel(release_dict)
	create(db_release)
	if db_release.id:  # 根据有没有生成新的id判断是否插入成功
		return response_code.resp_200(db_release.to_dict())
	else:
		return response_code.resp_400(message="发布单创建失败")


@router.post("/upload", name="自动发布版本-程序入版本仓库")
async def auto_distribute(release_info: release_schemas.CreateRelease):
	return "自动发布"


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
