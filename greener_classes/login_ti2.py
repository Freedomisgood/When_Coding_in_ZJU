import json
import time
from loginUtils import SSOLogin


class Ti(SSOLogin):
    def get_all_exams(self):
        params = (
            ('t', int(round(time.time() * 1000))),
            ('flag', 'true'),
        )

        response = self.sess.get("http://regi.zju.edu.cn/grs-pro/config/questions/getAQExamIds",
                                 params=params, verify=False)
        return response.json().get("ids")

    def get_all_exams_info(self, exmas: list):
        self.sess.headers.update({'Content-Type': 'application/json; charset=UTF-8', })
        response = self.sess.post('http://regi.zju.edu.cn/grs-pro/config/questions/getExamsByIds',
                                  data=json.dumps(exmas), verify=False)
        return response.json().get("exams")

    def finish_exam(self):
        params = (
            ('t', int(round(time.time() * 1000))),
            ('type', 'aqcs'),
            # 自定义成绩
            ('value', '98'),
            ('active', '10'),
        )

        response = self.sess.post('http://regi.zju.edu.cn/grs-pro/stu/processinfo/updateInfo',
                                 params=params, verify=False)
        print("推进下一步", response.text)
        return response.status_code == 200

    def run(self):
        exam_ids = self.get_all_exams()
        exams = self.get_all_exams_info(exam_ids)
        print("总共{}题".format( len(exams)))
        self.finish_exam()

if __name__ == '__main__':
    t = Ti(username="22151221", password="cl123123")
    t.sso_login()
    t.run()
