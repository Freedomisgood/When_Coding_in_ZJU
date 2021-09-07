#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/9/7 13:32
# @Author  : Mrli
# @File    : guide_class_login.py
import time
from loginUtils import SSOLogin


class GuideClass(SSOLogin):
    def getAllCourses(self):
        params = (
            ('t', str(int(round(time.time() * 1000)))),
            ('title', ''),
            ('isRequired', ''),
        )
        response = self.sess.get('http://regi.zju.edu.cn/grs-pro/config/vclassesdetail/queryList',
                                 params=params, verify=False)
        return response.json().get("list")

    def passClass(self, class_id: str) -> None:
        self.sess.headers["Referer"] = 'http://regi.zju.edu.cn/classDetail?id={}'.format(class_id)
        params = (
            ('t', str(int(round(time.time() * 1000)))),
            ('studyTime', str(1000)),
            ('classId', class_id),
        )
        response = self.sess.post('http://regi.zju.edu.cn/grs-pro/stu/classinfo/addStudyLog',
                                  params=params, verify=False)
        print(response.text)

    def run(self):
        self.sso_login()
        all_courses = self.getAllCourses()
        for c in all_courses:
            self.passClass(c.get("id"))


if __name__ == '__main__':
    # if len(sys.argv) < 2:
    #     print("请输入学号、密码")
    # username, password = sys.argv[1], sys.argv[2]
    in_str = input("请输入学号、密码(空格分割):").split()
    if len(in_str) == 2:
        username, password = in_str
    else:
        raise Exception("请分别输入学号与密码(空格分割)")

    gc = GuideClass(username, password)
    gc.run()
