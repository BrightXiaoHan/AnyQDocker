# 配置部署指南
（以下所有命令均在源代码根目录下执行）

## 环境搭建
- 根据[官方文档](./README.md)将环境部署在docker中，并编译成功。
- `build`目录下运行`run_server`并请求测试成功。
- 测试成功后关闭run_server程序

## 增加solr字段robot_id
增加该字段用于区分不同机器人的知识库

新建`build/faq/add_robot_id`文件修改为
```
[
    {
        "indexed": true,
        "stored": true,
        "type": "string",
        "name": "robot_id"
    }
]
```
新建`build/faq/add_answer_id`文件修改为
```
[
    {
        "indexed": false,
        "stored": true,
        "type": "string",
        "name": "answer_id"
    }
]
```
清理collection并重新设置schema
```bash
# 清理schema
python build/solr_script/solr_api.py clear_doc localhost collection1 8900

# 重新配置schema（注意该命令运行一次新的字段已经添加，再次运行会报错）
python build/solr_script/solr_api.py set_schema localhost collection1 build/faq/schema_format 8900
python build/solr_script/solr_api.py set_schema localhost collection1 build/faq/add_robot_id 8900
python build/solr_script/solr_api.py set_schema localhost collection1 build/faq/add_answer_id 8900
```

## 修改anyq检索插件的配置
`build/example/conf/retrieval.conf`文件修改为
```
retrieval_plugin {
    name : "term_recall_1"
    type : "TermRetrievalPlugin"
    search_host : "127.0.0.1"
    search_port : 8900
    engine_name : "collection1"
    solr_result_fl : "id,question,answer,answer_id"
    solr_q : {
        type : "EqualSolrQBuilder"
        name : "equal_solr_q_1"
        solr_field : "question"
        source_name : "question"
    }
    solr_q : {
        type : "EqualSolrQBuilder"
        name : "equal_solr_q_1"
        solr_field : "robot_id"
        source_name : "robot_id"
    }
    num_result : 15
}
```

## 启动anyq服务
```bash
cd build
./run_server
```