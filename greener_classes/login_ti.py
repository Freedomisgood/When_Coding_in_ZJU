import requests
import json
import time
from zju_login import ZJULogin


cookies = {
    'JSESSIONID': 'DB254B2A174D61FDB033A2333BDB2037',       #
    'Qs_lvt_292926': '1619495274',
    'Qs_pv_292926': '182399785585604800',
    '_pm0': 'jRckSHvo34%2FTAWDSQWWm3fct5DKIt2jVk0QuOMs23J4%3D',
    'sudyLoginToken': 'expired',
    '_csrf': 'S8mwplVi9KWoF2WQ0TlCeECiztJvZcCj3A0oCN6DA7I%3D',
    #
    '_pv0': 'Ze%2Bw4%2Bu2yeiYe%2F5kUE5HS4rlUJH5a2BE5dN2AXfzQ8CFwJ%2FNpQC%2Bv65O3Kf1ujBDuBjVROqdrZaXhEA0R4C2tWdOdBs8RBNeWpoOWbeTNubvHYTW5lwlwVVrp9qnMM1gQpm0nPQnAUiy98TXb9uyVwBC3SX%2FJBDyzdt30f2XQ4lMtGfjdNywXwDDVH1V4RAJ7M%2BRFf1iinqVgRQzZA%2FgPuIQFDFXjMXw72YVtxRXVhY0KZ35WvZpVfQkgW4gHkoMG8XK41F6aA7PHs9r28kbTwl3RcLt1AWwHeBl73nJbhhIYU5wT8mq1sj9gGM5TzzxFNbEPcrAVkZrH7MRJoZbMM5LKu%2FuQGFhu5O1%2Bu0Cfr1Y0nhCeCkvnsGtgITfLMIpNmlCtDuin1WXAnxRkw5%2FvrKB3K%2B5HaBSjgEOgPZvKzY%3D',
    '_pf0': 'XAFmdQYumpYqCWLjSboe79K8vB4%2Fwzzr0ebiTFZEmME%3D',
    '_pc0': '9wE8G%2Bo82PYhmhy5BhNMq0QwAO4mhJ8orJ7Vgjp5e5g%3D',
    #
    'iPlanetDirectoryPro': 'eHAWwGNKIVcNhDkPrBvv%2FzuKu69JTe1nDwGmHX8ZOFDqCC0Sr1lEaGxTaN1maMRn9mQgGd4sqTDq6uc75hLnN1IIDkQiVEL8DI%2FpPqtC7%2BiKiI0Fdh46KUdFEnN3yOyBgThCevKrYa%2BJgiCg07X8hn3AKX4lArUQou9%2Br%2Fw1mxUWhzhZ%2FK6swzCrrYJxgyEF5aOnVKy8JDNF5CVn8L%2FuhRyLl41l5Pe1Isb8EWfbLKhUz%2BpLlFA6YxtdMbYoo%2BqM2RV%2B%2FX%2FBjA7pU1rSEZ920bIUxp10SpHZZioC7EoT8Xd58Plb8sdhDz%2FVKAZ6H7pyKM3y%2BSwmoao38%2BE9i1D1FMSBmJB9CSQobNL8%2F3SfFdk%3D',
    #
    'stu-token': '3bdc205c024dabfc0d2bb235cdf6a9f0',
}

headers = {
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'Accept': 'application/json, text/plain, */*',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
    'token': '3bdc205c024dabfc0d2bb235cdf6a9f0',        #
    'Referer': 'http://regi.zju.edu.cn/process',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
}


def judge_has_exams():
    response = requests.get('http://regi.zju.edu.cn/grs-pro/stu/examstate/checkHasExam', headers=headers,
                            cookies=cookies, verify=False)
    json_data = response.json()
    if json_data.get("code") == 401: raise Exception(json_data.get("msg"))
    return json_data.get("flag")


def get_last_final_exam_id():
    response = requests.get('http://regi.zju.edu.cn/grs-pro/stu/examinfo/getFinalExam', headers=headers,
                            cookies=cookies, verify=False)
    return response.json().get("index")


def get_all_exams():
    params = (
        ('t', int(round(time.time() * 1000))),
        ('flag', 'true'),
    )

    response = requests.get('http://regi.zju.edu.cn/grs-pro/config/questions/getMutExamsIds', headers=headers,
                            params=params, cookies=cookies, verify=False)
    # print(response.json())
    return response.json().get("ids")


def get_all_exams_info(exmas: list):
    new_headers = headers.update({'Content-Type': 'application/json; charset=UTF-8',})
    response = requests.post('http://regi.zju.edu.cn/grs-pro/config/questions/getMutExamsByIds', headers=headers,
                             cookies=cookies, data=json.dumps(exmas), verify=False)
    return response.json().get("exams")


def submit(exam_info):
    selected = exam_info.get("answer").split(",")
    data = {
        "analysis": exam_info.get("analysis"),
        "answer": exam_info.get("answer"),
        "answers": exam_info.get("answers"),
        "flag": exam_info.get("flag"),
        "id": exam_info.get("id"),
        "indexs": exam_info.get("indexs"),
        "question": exam_info.get("question"),
        "selected": exam_info.get("selected"),  # None
        # 选中的答案
        "selecteds": selected,
        "t": int(round(time.time() * 1000)),
    }
    response = requests.post('http://regi.zju.edu.cn/grs-pro/stu/examstate/commitExam', headers=headers,
                             cookies=cookies, data=json.dumps(data), verify=False)
    # 每做完题更新状态, 前端用到, 这里不需要
    # response = requests.post('http://regi.zju.edu.cn/grs-pro/stu/examstate/updateNextExam', headers=headers,
    # 						 cookies=cookies, data=json.dumps(data), verify=False)
    # print(response.text)
    print("题目{}:{}, {}".format(exam_info.get("id"), exam_info.get("question"), response.json().get("msg")))


def finish_exam():
    params = {
        't': int(round(time.time() * 1000)),
        'type': 'qybh',
        'value': '1',
        'active': '9',
    }

    response = requests.post('http://regi.zju.edu.cn/grs-pro/stu/processinfo/updateInfo', headers=headers,
                             params=params, cookies=cookies, verify=False)
    print("推进下一步", response.text)


if __name__ == '__main__':
	# 是否还有题目未做完
    reminded = judge_has_exams()
    if reminded:
        last_id = get_last_final_exam_id()
        print("当前最新做到：", last_id)
        exam_ids = get_all_exams()
        exams = get_all_exams_info(exam_ids)
        for e_data in exams:
            # print(e_data)
            submit(e_data)
        finish_exam()
