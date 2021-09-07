import json
import time
from zju_login import ZJULogin
import urllib.parse as urlparse


class Ti(ZJULogin):
    def judge_has_exams(self):
        response = self.sess.get('http://regi.zju.edu.cn/grs-pro/stu/examstate/checkHasExam',
                                 verify=False)
        json_data = response.json()
        if json_data.get("code") == 401: raise Exception(json_data.get("msg"))
        return json_data.get("flag")

    def get_last_final_exam_id(self):
        response = self.sess.get('http://regi.zju.edu.cn/grs-pro/stu/examinfo/getFinalExam',
                                 verify=False)
        return response.json().get("index")

    def get_all_exams(self):
        params = (
            ('t', int(round(time.time() * 1000))),
            ('flag', 'true'),
        )

        response = self.sess.get('http://regi.zju.edu.cn/grs-pro/config/questions/getMutExamsIds',
                                 params=params, verify=False)
        return response.json().get("ids")

    def get_all_exams_info(self, exmas: list):
        # new_headers = headers.update({'Content-Type': 'application/json; charset=UTF-8',})
        self.sess.headers.update({'Content-Type': 'application/json; charset=UTF-8', })
        response = self.sess.post('http://regi.zju.edu.cn/grs-pro/config/questions/getMutExamsByIds',
                                  data=json.dumps(exmas), verify=False)
        return response.json().get("exams")

    def submit(self, exam_info):
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
        response = self.sess.post('http://regi.zju.edu.cn/grs-pro/stu/examstate/commitExam',
                                  data=json.dumps(data), verify=False)
        # 每做完题更新状态, 前端用到, 这里不需要
        # response = self.sess.post('http://regi.zju.edu.cn/grs-pro/stu/examstate/updateNextExam', 
        # 						 data=json.dumps(data), verify=False)
        # print(response.text)
        print("题目{}:{}, {}".format(exam_info.get("id"), exam_info.get("question"), response.json().get("msg")))

    def finish_exam(self):
        params = {
            't': int(round(time.time() * 1000)),
            'type': 'qybh',
            'value': '1',
            'active': '9',
        }

        response = self.sess.post('http://regi.zju.edu.cn/grs-pro/stu/processinfo/updateInfo',
                                  params=params, verify=False)
        print("推进下一步", response.text)
        return response.status_code == 200

    def run(self):
        # 是否还有题目未做完
        reminded = self.judge_has_exams()
        if reminded:
            last_id = self.get_last_final_exam_id()
            print("当前最新做到：", last_id)
            exam_ids = self.get_all_exams()
            exams = self.get_all_exams_info(exam_ids)
            for e_data in exams:
                # print(e_data)
                self.submit(e_data)
            self.finish_exam()

    def sso_login(self):
        """
        获得token，并在请求头上加上token
        Returns: token
        """
        def substract_query_params(url):
            parsed = urlparse.urlparse(url)
            querys = urlparse.parse_qs(parsed.query)
            return {k: v[0] for k, v in querys.items()}

        def get_code():
            params = (
                ('response_type', 'code'),
                ('client_id', 'kU3pGMMUuXK3zFmnMY'),
                ('redirect_uri', 'http://regi.zju.edu.cn/ssologin'),
            )

            response = self.sess.get('https://zjuam.zju.edu.cn/cas/oauth2.0/authorize', params=params)
            location = ""
            for r in response.history:
                if "location" in r.headers:
                    location = r.headers.get("location")
            return substract_query_params(location).get("code")

        # 获得cookies
        self.login()
        # 获得sso_login所需的code
        code = get_code()
        params = (
            ('t', int(round(time.time() * 1000))),
            ('code', code),
            ('role', 'student'),
        )
        response = self.sess.get('http://regi.zju.edu.cn/grs-pro/zs/auth/ssoLogin', params=params, verify=False)
        token = response.json().get("token")
        self.sess.headers["token"] = token
        return token


if __name__ == '__main__':
    t = Ti(username="22151221", password="cl123123")
    t.sso_login()
    t.run()
