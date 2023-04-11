## 一、创建异步事件函数
1. 创建函数
2. 使用内置运行时创建
3. 函数名称：async_http
4. 请求处理程序类型：处理事件请求
5. 运行环境：Python 3.9
6. 使用示例代码
7. 创建完成后，点击函数代码，查看函数代码，复制 ```async_task.py```中的代码
8. 点击部署代码

## 二、创建http函数
1. 创建函数
2. 使用自定义运行时创建
3. 函数名称：feishu_access
4. 请求处理程序类型：处理http请求
5. 运行环境：Python 3.10
6. 使用示例代码
7. 创建完成后，点击函数代码，查看函数代码，复制 ```http.py```中的代码
8. 点击部署代码
9. 函数配置，添加环境变量
  - ALIYUN_ACCESS_KEY_ID: 阿里云的 accessKeyId
  - ALIYUN_ACCESS_KEY_SECRET: 阿里云的 accessKeySecret
  - ALIYUN_FC_ASYNC_TASK_SERVICE_NAME: async_http 函数所在的服务名
  - ALIYUN_FC_ASYNC_TASK_FUNCTION_NAME: async_http 函数的名字，即为 async_http
  - ALIYUN_FC_ENDPOINT: 如 12345.cn-hangzhou.fc.aliyuncs.com，参考 https://help.aliyun.com/document_detail/52984.html
  - FEISHU_CHATGPT_BASE_URL: feishu-chatgpt 里提供的链接，如 https://xxxxx.fcapp.run，注意，不要后面的 /webhook/xxx
  - FEISHU_ENCRYPT_KEY: 飞书应用事件订阅里的 Encrypt Key

## 三、飞书配置更改
1. 飞书事件订阅里的请求地址变更为二中的触发器管理里的地址
2. 飞书机器人里的消息卡片请求网址变更为二中的触发器管理里的地址