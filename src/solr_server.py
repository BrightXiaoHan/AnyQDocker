from collections import defaultdict
import json
import traceback

import tornado
from tornado.web import RequestHandler

import anyq_tools as anyq
import solr_yuyi_tools as tools


class SolrToolsHandler(RequestHandler):

    def post(self):
        data = json.loads(self.request.body.decode("utf-8"))
        result_data = {}
        try:
            code = self._handle_data(data)
            result_data["status_code"] = code
        except Exception as e:
            result_data["status_code"] = "500"
            result_data["msg"] = str(e) + traceback.format_exc()

        self.write(json.dumps(result_data, ensure_ascii=False))

    def _handle_data(self, dic):
        """处理字典数据

        Args:
            dic (dict): 字典数据，具体类型子类指定

        Raises:
            NotImplementedError: 子类必须复写该方法

        Returns:
            int: 状态码
        """
        raise NotImplementedError


class CreateRobotHandler(SolrToolsHandler):
    """数据示例{
        "robot_code": "robot_id"
    }
    """

    def _handle_data(self, dic):
        return 0


class DeleteRobotHandler(SolrToolsHandler):
    """数据示例{
        "robot_code": "robot_id"
    }
    """

    def _handle_data(self, dic):

        return tools.delete_robot(dic["robot_code"])


class DeleteItemsHandler(SolrToolsHandler):
    """数据示例{
        "q_ids": ["id1", "id2"],
        "robot_code": "robot_id"
    }
    """

    def _handle_data(self, dic):
        return tools.delete_documents(dic["q_ids"])


class AddItemsHandler(SolrToolsHandler):
    """数据示例{
        "documents":[{"answer": "支持推广账户使用。", "question": "AI服务支持推广账号使用么？", "id": "3"}],
        "robot_id": "robot_id"
    }
    """

    def _handle_data(self, dic):
        return tools.upload_documents(documents=dic["documents"], robot_id=dic["robot_id"])


# 双级字典，第一级，key:robot_id, value dict， 二级字典 key: question, value
hot_question_cache = defaultdict(lambda: defaultdict(int))


def get_hotest_questions(robot_code, top=5):
    if len(hot_question_cache[robot_code]) == 0:
        return []

    questions = sorted(
        hot_question_cache[robot_code], key=lambda x: hot_question_cache[robot_code][x])
    return questions[:top]


class AskHandler(RequestHandler):
    """数据示例{
        "robot_code": "test_robot_id",
        "question": "用户提问的问题"
    }
    """

    def post(self):
        data = json.loads(self.request.body.decode("utf-8"))
        result = anyq.ask(data["question"], data["robot_code"])
        response_json = {
            "answer": "对不起，您问的问题我暂时无法回答，但是我会努力学习的哦。",
            "ask_code": data["question"],
            "answer_code": "99999",
            "answer_type": -1,
            "confidence": 0,
            "hotQuestions": get_hotest_questions(data["robot_code"]),
            "recommendQuestions": []
        }
        if len(result) > 0:
            hot_question_cache[data["robot_code"]][result[0]["question"]] += 1
            response_json["answer"] = result[0]["answer"]
            response_json["ask_code"] = result[0]["qa_id"]
            response_json["confidence"] = result[0]["confidence"]
            json_info = json.loads(result[0]["json_info"])
            response_json["answer_code"] = json_info.get(
                "answer_id", response_json["ask_code"])
            response_json["answer_type"] = 0  # 正常答案
        for item in result[1:]:
            response_json["recommendQuestions"].append(item["question"])
        self.write(json.dumps(response_json, ensure_ascii=False))


def main():
    # 对服务的配置问题
    settings = {
        'debug': False
    }
    application = tornado.web.Application([
        (r'/robot_manager/single/add_items', AddItemsHandler),
        (r'/robot_manager/single/delete_items', DeleteItemsHandler),
        (r'/robot_manager/single/delete_robot', DeleteRobotHandler),
        (r'/robot_manager/single/create_robot', CreateRobotHandler),
        (r'/robot_manager/single/ask', AskHandler)
    ], **settings)
    http_server = tornado.httpserver.HTTPServer(application)
    # 2. 服务端口
    http_server.listen(8080)
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()
