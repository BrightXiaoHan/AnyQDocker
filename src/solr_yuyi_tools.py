import requests
import json

def query_documents(query, host="localhost", enginename="collection1", port=8900):
    """请求文档
    
    Args:
        query (str): solr 请求。示例：q=question:你好
        host (str, optional): solr服务地址. Defaults to "localhost".
        enginename (str, optional): engine名称. Defaults to "collection1".
        port (int, optional): solr服务端口. Defaults to 8900.
    Returns:
        list: solr数据集合。示例: [{'_version_': 1654033669784862720, 'answer': '支持推广账户使用。', 'id': 'test_unique_id', 'question': '你好', 'robot_id': 'test_robot_id'}]
    """
    url = "http://{}:{}/solr/{}/select?q={}&wt=json".format(host, port, enginename, query)
    response = requests.get(url)
    data = json.loads(response.text)
    
    return data['response']['docs']

def excute_json_query(query, host="localhost", enginename="collection1", port=8900):
    """执行json请求
    
    Args:
        query (list or dict): json请求。示例 {"delete": ["test_unique_id"]}
        robot_id (str): 机器人的名称
        host (str, optional): solr服务地址. Defaults to "localhost".
        enginename (str, optional): engine名称. Defaults to "collection1".
        port (int, optional): solr服务端口. Defaults to 8900.

    Returns:
        int: 0表示上传成功，否则代表上传失败
    """
    url = "http://{}:{}/solr/{}/update".format(host, port, enginename)
    response = requests.post(url, json=query)
    data = json.loads(response.text)
    return data['responseHeader']['status']

def upload_documents(documents, robot_id, host="localhost", enginename="collection1", port=8900):
    """上传文档
    
    Args:
        documents (list): 文档列表。示例 [{"answer": "支持推广账户使用。", "question": "AI服务支持推广账号使用么？", "id": "3", "answer_id": "test_answer_id}]
        robot_id (str): 机器人的名称
        host (str, optional): solr服务地址. Defaults to "localhost".
        enginename (str, optional): engine名称. Defaults to "collection1".
        port (int, optional): solr服务端口. Defaults to 8900.

    Returns:
        int: 0表示上传成功，否则代表上传失败
    """
    for doc in documents:
        doc.update({"robot_id": robot_id})
    return excute_json_query(documents, host, enginename, port)

def delete_documents(ids, host="localhost", enginename="collection1", port=8900):
    """删除文档
    
    Args:
        documents (list): id列表。示例 ["1", "2"]
        robot_id (str): 机器人的名称
        host (str, optional): solr服务地址. Defaults to "localhost".
        enginename (str, optional): engine名称. Defaults to "collection1".
        port (int, optional): solr服务端口. Defaults to 8900.

    Returns:
        int: 0表示删除成功，否则代表删除失败
    """
    documents = {
        "delete": ids
    }
    return excute_json_query(documents, host, enginename, port)

def delete_robot(robot_id, host="localhost", enginename="collection1", port=8900):
    """删除某个机器人下的所有文档
    
    Args:
        robot_id (str): 机器人的名称
        host (str, optional): solr服务地址. Defaults to "localhost".
        enginename (str, optional): engine名称. Defaults to "collection1".
        port (int, optional): solr服务端口. Defaults to 8900.

    Returns:
        int: 0表示删除成功，否则代表删除失败
    """
    candidates = query_documents("robot_id:" + robot_id, host, enginename, port)
    ids = [item["id"] for item in candidates if item["robot_id"] == robot_id]
    if len(ids) == 0:
        return 0
    return delete_documents(ids, host, enginename, port)

    