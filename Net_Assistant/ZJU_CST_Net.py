import requests
import hashlib
import json
import os


headers = {
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': '*/*',
    'Origin': 'http://192.0.0.6',
    'Referer': 'http://192.0.0.6/index.html?url=http://www.msftconnecttest.com/redirect',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}


def get_password(in_s):
    s = in_s.encode("utf8")
    res = hashlib.md5(s).hexdigest()
    start_index = 8
    length = 16
    return res[start_index: length+start_index]


class ResultData:
    """
    解析文本=>返回结果类
    """
    def __init__(self, msg, code):
        self.msg = msg
        self.code = code

    @staticmethod
    def match(msg):
        if msg.isalnum():
            return ResultData(msg="登录成功", code=200)
        elif msg == "logout_ok":
            return ResultData(msg="注销成功", code=200)
        elif msg == "logout_error":
            return ResultData(msg="注销失败, 没有在线设备", code=400)
        elif msg == "online_num_error":
            return ResultData(msg="登录失败, 在线设备超时", code=400)
        elif msg == "username_error":
            return ResultData(msg="登录失败, 账号密码错误", code=400)
        else:
            return ResultData(msg="未知消息类型", code=400)

    def to_json(self):
        return {"msg": self.msg, "code": self.code}

    def __str__(self):
        return str(self.to_json())


class ZJUOnline:
    @staticmethod
    def login(stu_id: str, pwd: str):
        """
        登录
        # online_num_error ==> 超时Error
        # 10784662880456   ==> 登录成功显示
        """
        data = {
          'username': stu_id,
          'password': get_password(pwd),
          'drop': '0',
          'type': '1',
          'n': '100'
        }
        response = requests.post('http://192.0.0.6/cgi-bin/do_login', headers=headers, data=data, verify=False)
        print(response.text)
        return ResultData.match(response.text)

    @staticmethod
    def logout(stu_id: str, pwd: str):
        """
        注销：只要密码正确，就能使其他设备下线
       # logout_ok     ==> 注销成功
        # logout_error  ==> 没有上线设备
        """
        data = {
          'username': stu_id,
          'password': pwd,
          'drop': '0',
          'type': '1',
          'n': '1'
        }
        response = requests.post('http://192.0.0.6/cgi-bin/force_logout', headers=headers, data=data, verify=False)
        return ResultData.match(response.text)


account = "22151221"
pwd = "zjucst"

if __name__ == "__main__":
    # 账号池有两种方式维护： 
    #   1.账号信息放在配套的本地配置文件中==>随机碰撞找到空闲账号
    #   2.账号信息放在服务器上，通过http请求空闲账号==>通过服务器管控，登出时需要反馈给服务器
    # 如果没有空闲账号，则强迫登录自己账号的设备下线，使自己上线
    f_name = "account.json"

    if account == "" or pwd == "":
        if not os.path.exists(f_name):
            with open(f_name, "w") as f:
                account, pwd = input("请输入账号, 密码").split()
                json.dump({"account": account, "password": pwd}, f)
        else:
            with open(f_name, "r") as f:
                d = json.load(f)
                account, pwd = d.get("account"), d.get("password")
    
    # 登录前把其他设备下线
    res = ZJUOnline.logout(account, pwd)
    res = ZJUOnline.login(account, pwd)
    print(res)