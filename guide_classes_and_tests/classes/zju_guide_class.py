from copy import copy
import argparse

import requests
import time

JSESSIONID = "*"
stu_token = "*"
# token = "*"   // 不用填

cookies = {
    'JSESSIONID': JSESSIONID,
    'Qs_lvt_292926': '1619495274',
    'Qs_pv_292926': '182399785585604800',
    '_csrf': 'S8mwplVi9KWoF2WQ0TlCeEh8aBlgVLBgLOUa6g8JMPw%3D',
    '_pv0': 'ywLMJMeXPh%2FykjNV24jkfxh6mFAUfILtoDzkLX%2F96x7Jpv%2BHFgCSGimzOFr2hrCm2AIG2pQQucyMR8wxROGowuPj0RGFM3v9%2BlqshxvqV3l2B89KLL4D27cJ68npMhwJAl8D8u0dS0u9cp4WYP7B7L474Tl%2BOKwJ47RJv3NrPvkrfme7t80z2hdpAegSDjSzVNZkk5h75lJwrgfKsrZcZb9ItULZB65G8d6fgbJr6ONTUXZTxECppk%2BCq7jX3bhnqF6GCwtCCb94YliNhx0Y0jKUnFRMKSgCr5ClNuVQ67uoT00wqMqVYwvF6%2BagcPBECJpBGplicjoUh62c7BaZuqvQdBxYxyD4wP7nHm2NgC2vGfGBLRl2rrh018Y7YRYmP9XnpLWw5UnYeSVGeFiWc6HPAMfSVYqUKd949HvYDnQ%3D',
    '_pf0': '6GgR2KbEHBQWjpDcUa6X7cyxbW9y7bFDd3RvfkoeIUI%3D',
    '_pm0': 'jRckSHvo34%2FTAWDSQWWm3fct5DKIt2jVk0QuOMs23J4%3D',
    '_pc0': '9wE8G%2Bo82PYhmhy5BhNMq6v4gKfPw6OG2cC5CkK4dLc%3D',
    'iPlanetDirectoryPro': 'UKkZdfFnupZh%2BFiz8Oqo67cZJGGo%2FPl6Ku%2BrT0hrFezltEfo9TfZa8T%2FA%2F2KQn9npzcTwBagl6DGpRr7Efqr1Qvdrj8fBsrTl%2BcULGim%2FlB%2FcUEzgxrOKJ2ygcCiMt6oIgRxQQbqc4NDJhkn5Kq9Delpp3gsYQMN60wsgRK7S%2FUhG9rOZG11S6KmFqBGWTh%2B03JVS7DTId1O5MYWrq%2B3I1291xbEgLYhGs5tASy3VJgYtqmzFgozWeJrn6yB1cAknSAfBK2iryN7ksTW3Acv5Oys3slK5ucfgiSCMCDEhLdX883lvMV%2BYomLLxsSIRlGOcuS1SONzF0DYGriuzTaT353Np%2BXO10xRghb0ShXwEI%3D',
    'pageType': '',
    'stu-token': stu_token,
}

headers = {
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'Accept': 'application/json, text/plain, */*',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
    # 'token':token ,
    'Referer': 'http://regi.zju.edu.cn',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
}


def getAllCourses():
    params = (
        ('t', str(int(round(time.time() * 1000)))),
        ('title', ''),
        ('isRequired', ''),
    )
    response = requests.get('http://regi.zju.edu.cn/grs-pro/config/vclassesdetail/queryList', headers=headers,
                            params=params, cookies=cookies, verify=False)
    return response.json().get("list")


def passClass(class_id: str) -> None:
    pass_header = copy(headers)
    pass_header["Referer"] = 'http://regi.zju.edu.cn/classDetail?id={}'.format(class_id)
    params = (
        ('t', str(int(round(time.time() * 1000)))),
        ('studyTime', str(1000)),
        ('classId', class_id),
    )
    response = requests.post('http://regi.zju.edu.cn/grs-pro/stu/classinfo/addStudyLog', headers=pass_header,
                             params=params, cookies=cookies, verify=False)
    print(response.text)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="先访问 http://regi.zju.edu.cn/classes \
                                                登录账号后后打开开发者工具(Chrome为F12快捷键) \
                                                 然后将Application菜单栏下Storage->cookies中的stu_token和\
                                                 JSESSIONID对应输入为本程序的参数")
    parser.add_argument("-s", "--JSESSIONID", help="Cookies中的JSESSIONID字段", required=True)
    parser.add_argument("-t", "--stu_token", help="Cookies中的stu_token字段", required=True)
    args = parser.parse_args()

    JSESSIONID = args.JSESSIONID
    stu_token = args.stu_token
    all_courses = getAllCourses()
    for c in all_courses:
        passClass(c.get("id"))
