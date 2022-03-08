# 基于Zentao的CI集成
##项目架构说明
- app 应用程序主目录
  - db sqlAlchemy与数据库的连接创建
  - models 数据库模型（表结构）
  - routers 接口定义及路由
    - business 开头的表示业务功能接口
    - bug、build、test_task等的表/视图的CRUD接口
    - tools 工具接口
    - CD CD服务端接口
  - schemas 引用pydantic模型：入参类型的校验等功能；与router模块一一对应
  - utils 通用工具模块
    - compress 压缩
    - compress 压缩
    - custom_log 自定义日志模块，引用loguru，用于所有业务代码的日志
    - file_handle 文件处理模块
    - html2string HTML内容转化成String，主要用于测试单、测试报告、发布单的HTML构建
    - json_rw  json文件的读写，主要用于客户端注册时的CDClientInfo.json的读写
    - log_handle 引用loguru，主要重新定义fastapi的日志格式
    - response_code 所有接口响应的代码定义
    - z_mail 邮件发送封装，引用zmail，用于自动邮件通知的业务
  - config.py 程序的参数配置
  - static  文件夹，所有静态文件如html模板、json配置信息
  - main.py 主程序，启动入口
