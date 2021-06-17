import json
import time
import requests


CREATE_ROBOT = "http://localhost:8080/robot_manager/single/create_robot"
ADD_ITEMS = "http://localhost:8080/robot_manager/single/add_items"
DELETE_ITEMS = "http://localhost:8080/robot_manager/single/delete_items"
DELETE_ROBOT = "http://localhost:8080/robot_manager/single/delete_robot"
ASK = "http://localhost:8080/robot_manager/single/ask"
ROBOT_CODE = "test_robot_id"
SLEEP_TIMES = 10


def post_get_data(url, request_data):
    """post方法请求url，并解析返回参数

    Args:
        url (str): 待请求api的url
        request_data (dict): 请求参数

    Return:
        dict: api返回结果的json解析结果，为python字典格式
    """
    response = requests.post(url, json=request_data)
    data = json.loads(response.text)
    print(data)
    return data


def test_case_one():
    # create robot
    response = post_get_data(CREATE_ROBOT, {"robot_code": ROBOT_CODE})
    assert response["status_code"] == 0

    # add some data
    response = post_get_data(ADD_ITEMS, {
        "documents": [
            {
                "answer": "测试答案1",
                "question": "这台苹果多少钱",
                "id": "test_question_id_1",
                "answer_id": "answer_id"
            },
            {
                "answer": "测试答案2",
                "question": "今天天气怎么样",
                "id": "test_question_id_2",
                "answer_id": "answer_id"
            },
            {
                "answer": "测试答案2",
                "question": "今天天气怎么样",
                "id": "test_question_id_3",
                "answer_id": "answer_id"
            }
        ],
        "robot_id": ROBOT_CODE
    })
    assert response["status_code"] == 0

    # ask questions
    time.sleep(SLEEP_TIMES)
    response = post_get_data(ASK, {
        "robot_code": ROBOT_CODE,
        "question": "今天天气怎样"
    })
    assert response["answer"] == "测试答案2"
    assert len(response["recommendQuestions"]) > 0

    # delete items
    response = post_get_data(DELETE_ITEMS, {
        "q_ids": ["test_question_id_2", "test_question_id_3"],
        "robot_code": ROBOT_CODE
    })
    assert response["status_code"] == 0

    # ask questions
    time.sleep(SLEEP_TIMES)
    response = post_get_data(ASK, {
        "robot_code": ROBOT_CODE,
        "question": "今天天气怎样"
    })
    assert response["answer_type"] == -1

    # delete_robot
    response = post_get_data(DELETE_ROBOT, {
        "robot_code": ROBOT_CODE
    })
    assert response["status_code"] == 0

    # ask questions
    time.sleep(SLEEP_TIMES)
    response = post_get_data(ASK, {
        "robot_code": ROBOT_CODE,
        "question": "这台苹果多少钱"
    })
    assert response["answer_type"] == -1


def main():
    test_case_one()


if __name__ == "__main__":
    main()
