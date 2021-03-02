# 一问一答机器人web api接口
调用接口时请根据部署情况调整api的ip与端口

**启动服务的命令**
```bash
python3 tools/robot_manager/solr_server.py
```

**注：发送请求时根据机器人部署的服务器地址与端口对请求进行调整**

## 创建机器人
**http请求示例**
```http
POST http://localhost:8080/robot_manager/single/create_robot HTTP/1.1
Content-Type: application/json

{
    "robot_code": "你好"
}
```
**参数说明**
- robot_code: 机器人编号（唯一标识）

**http返回示例**
```http
HTTP/1.1 200 OK
Connection: close
Server: TornadoServer/6.0.1
Content-Type: text/html; charset=UTF-8
Date: Fri, 27 Dec 2019 07:18:17 GMT
Content-Length: 18

{
  "status_code": 0
}
```
**返回参数说明**
- status_code: 状态码，0为请求成功，其他状态码为请求失败

## 向机器人添加数据
**http请求示例**
```http
POST http://localhost:8080/robot_manager/single/add_items HTTP/1.1
Content-Type: application/json

{
    "documents":[
        {
            "answer": "测试答案", 
            "question": "测试问题", 
            "id": "test_question_id_1",
            "answer_id": "answer_id"
        },
        {
            "answer": "测试答案", 
            "question": "测试问题", 
            "id": "test_question_id_2",
            "answer_id": "answer_id"
        }
    ],
    "robot_id": "test_robot_id"
}
```
**参数说明**
- robot_code: 机器人编号（唯一标识）
- documents: 需要添加的文档，每个文档应该有question, answer, id字段。其中id字段一定要是全局唯一标识

**http返回示例**
```http
HTTP/1.1 200 OK
Connection: close
Server: TornadoServer/6.0.1
Content-Type: text/html; charset=UTF-8
Date: Fri, 27 Dec 2019 07:24:47 GMT
Content-Length: 18

{
  "status_code": 0
}
```
**返回参数说明**
- status_code: 状态码，0为请求成功，其他状态码为请求失败


## 删除机器人的某些数据
**http请求示例**
```http
POST http://localhost:8080/robot_manager/single/delete_items HTTP/1.1
Content-Type: application/json

{
    "q_ids": ["test_question_id_2"],
    "robot_code": "test_robot_id"
}
```
**参数说明**
- robot_code: 机器人编号（唯一标识）
- q_ids: 问答对的id列表，其中的id对应添加问答对时的id。其中id字段一定要是全局唯一标识

**http返回示例**
```http
HTTP/1.1 200 OK
Connection: close
Server: TornadoServer/6.0.1
Content-Type: text/html; charset=UTF-8
Date: Fri, 27 Dec 2019 07:24:47 GMT
Content-Length: 18

{
  "status_code": 0
}
```
**返回参数说明**
- status_code: 状态码，0为请求成功，其他状态码为请求失败

## 删除整个机器人
**http请求示例**
```http
POST http://localhost:8080/robot_manager/single/delete_robot HTTP/1.1
Content-Type: application/json

{
    "robot_code": "test_robot_id"
}
```
**参数说明**
- robot_code: 机器人编号（唯一标识）

**http返回示例**
```http
HTTP/1.1 200 OK
Connection: close
Server: TornadoServer/6.0.1
Content-Type: text/html; charset=UTF-8
Date: Fri, 27 Dec 2019 07:27:22 GMT
Content-Length: 18

{
  "status_code": 0
}
```
**返回参数说明**
- status_code: 状态码，0为请求成功，其他状态码为请求失败


## 向机器人提问
**http请求示例**
```http
POST http://localhost:8080/robot_manager/single/ask HTTP/1.1
Content-Type: application/json

{
    "robot_code": "test_robot_id",
    "question": "用户提问的问题"
}
```
**参数说明**
- robot_code: 机器人编号（唯一标识）
- data: 包含唯一字段question，为用户提问的问题

**http返回示例**
```http
HTTP/1.1 200 OK
Date: Mon, 30 Dec 2019 02:56:07 GMT
Content-Length: 26
Connection: close
Content-Type: text/html; charset=UTF-8
Server: TornadoServer/6.0.1

{
  "answer": "测试答案",
  "ask_code": "问题id",
  "answer_code": "答案id",
  "answer_type": 0,
  "confidence": 0.9756978750228882
}

```
**返回参数说明**
- answer: 问题答案
- ask_code: 匹配到问题的唯一编号
- answer_code: 匹配到答案的唯一编号
- answer_type: 答案类型。（0表示找到答案，1表示未找到答案）
- confidence: 答案置信度，浮点数

