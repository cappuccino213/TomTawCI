# 基于Zentao的CI集成
##项目架构说明
- app 应用程序主目录
  - db sqlAlchemy与数据库的连接创建
  - models 数据库模型（表结构）
  - routers 接口定义及路由
    - business 开头的表示业务功能接口，其他的未CRUD接口
  - schemas schemas模型，自带入参类型的校验等功能
  - utils 通用工具模块
  - config.py 参数配置
  - main.py 主程序，启动入口