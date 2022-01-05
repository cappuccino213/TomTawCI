"""
@File : business_product_project.py
@Date : 2021/11/23 10:16
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""

from fastapi import APIRouter
from app.db.database import execute_sql
from app.utils import response_code
from app.schemas import product_schemas


# 查询具体对照
def query_ppm(pp_dict: dict):
	# base_sql = """SELECT
	# 	product AS product_id,
	# 	pd.`name` AS product_name,
	# 	project AS project_id,
	# 	pj.`name` AS project_name,
	# 	pj.PM as project_owner
	# FROM
	# 	zt_projectproduct pp
	# 	LEFT JOIN zt_product pd ON pp.product = pd.id
	# 	LEFT JOIN zt_project pj ON pp.project = pj.id
	# WHERE
	# 	pd.deleted = '0'
	# 	AND pj.status != 'closed'
	# 	AND pj.deleted = '0'"""

	base_sql = """SELECT
	count( pj.`name` ),
	product AS product_id,
	pd.`name` AS product_name,
	project AS project_id,
	pj.`name` AS project_name,
	pj.PM AS project_owner,
	zt.account AS members 
FROM
	zt_projectproduct pp
	LEFT JOIN zt_product pd ON pp.product = pd.id
	LEFT JOIN zt_project pj ON pp.project = pj.id
	LEFT JOIN zt_team zt ON pp.project = zt.root 
WHERE
	pd.deleted = '0' 
	AND pj.STATUS != 'closed' 
	AND pj.deleted = '0'  
"""  # 增加团队成员也可以获取项目详情
	extra_sql = ''
	if pp_dict['product_id']:
		extra_sql += " AND product={}".format(pp_dict['product_id'])
	if pp_dict['product_name']:
		extra_sql += " AND pd.`name`='{}'".format(pp_dict['product_name'])
	if pp_dict['project_id']:
		extra_sql += " AND project={}".format(pp_dict['project_id'])
	if pp_dict['project_name']:
		extra_sql += " AND pj.`name`='{}'".format(pp_dict['project_name'])
	if pp_dict['project_owner']:
		extra_sql += " AND (pj.PM='{0}' OR zt.`account`='{0}')".format(pp_dict['project_owner'])
	extra_sql += "GROUP BY pj.`name`"  # 去重owner和member的值相同是or造成的重复值
	return execute_sql(base_sql + extra_sql)


router = APIRouter(prefix="/ewordci/get-product-project", tags=["base-info"])


@router.post("/mapping", response_model=product_schemas.ProductProjectMapping, name="获取产品-项目id与名称的对照")
async def product_project_mapping(ppm: product_schemas.ProductProjectMapping):  # 入参说明，在swagger的Request body可以体现
	res = query_ppm(ppm.dict())  # schemas转化成dict形式参数
	if res:
		return response_code.resp_200(res)
	else:
		return response_code.resp_404(message="未找到对应数据")


if __name__ == "__main__":
	# pass
	# pp = {"product_id": "", "product_name": "", "project_id": "", "project_name": "医学影像浏览器维护2021"}
	# print(query_ppm(pp))
	print(" AND pj.PM='{0}' OR zt.`account`='{0}'".format('wangjing'))
