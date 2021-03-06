import datetime
import json
import os
import random
import re
import time

import ddddocr
import requests

ocr = ddddocr.DdddOcr(det=False, ocr=True)


def cope_with_captcha(sess):
    """识别验证码"""
    response = sess.get('https://healthreport.zju.edu.cn/ncov/wap/default/code')
    # img_bytes = response.content
    # with open("captcha.png", "wb") as f:
    #     f.write(img_bytes)
    res = ocr.classification(response.content)
    return res.upper()


# ▲.在这里设置推送pushplus!
def push2pushplus(content, token=""):
    """
    推送消息到pushplus
    """
    if token == '':
        print("[注意] 未提供token，不进行pushplus推送！")
    else:
        server_url = f"http://www.pushplus.plus/send"
        params = {
            "token": token,
            "title": 'ZJU钉钉健康打卡',
            "content": content
        }

        response = requests.get(server_url, params=params)
        json_data = response.json()
        print(json_data)


class LoginError(Exception):
    """Login Exception"""
    pass


def get_day(delta=0):
    """
    获得指定格式的日期
    """
    today = datetime.date.today()
    oneday = datetime.timedelta(days=delta)
    yesterday = today - oneday
    return yesterday.strftime("%Y%m%d")


def take_out_json(content):
    """
    从字符串jsonp中提取json数据
    """
    s = re.search("^jsonp_\d+_\((.*?)\);?$", content)
    return json.loads(s.group(1) if s else "{}")


def get_date():
    """Get current date"""
    today = datetime.date.today()
    return "%4d%02d%02d" % (today.year, today.month, today.day)


class ZJULogin(object):
    """
    Attributes:
        username: (str) 浙大统一认证平台用户名（一般为学号）
        password: (str) 浙大统一认证平台密码
        sess: (requests.Session) 统一的session管理
    """
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
    }
    BASE_URL = "https://healthreport.zju.edu.cn/ncov/wap/default/index"
    LOGIN_URL = "https://zjuam.zju.edu.cn/cas/login?service=http%3A%2F%2Fservice.zju.edu.cn%2F"

    def __init__(self, username, password, delay_run=False):
        self.username = username
        self.password = password
        self.delay_run = delay_run
        self.sess = requests.Session()

    def login(self):
        """Login to ZJU platform"""
        res = self.sess.get(self.LOGIN_URL)
        execution = re.search(
            'name="execution" value="(.*?)"', res.text).group(1)
        res = self.sess.get(
            url='https://zjuam.zju.edu.cn/cas/v2/getPubKey').json()
        n, e = res['modulus'], res['exponent']
        encrypt_password = self._rsa_encrypt(self.password, e, n)

        data = {
            'username': self.username,
            'password': encrypt_password,
            'execution': execution,
            '_eventId': 'submit',
            "authcode": ""
        }
        res = self.sess.post(url=self.LOGIN_URL, data=data)
        # check if login successfully
        if '用户名或密码错误' in res.content.decode():
            raise LoginError('登录失败，请核实账号密码重新登录')
        print("统一认证平台登录成功~")
        return self.sess

    def _rsa_encrypt(self, password_str, e_str, M_str):
        password_bytes = bytes(password_str, 'ascii')
        password_int = int.from_bytes(password_bytes, 'big')
        e_int = int(e_str, 16)
        M_int = int(M_str, 16)
        result_int = pow(password_int, e_int, M_int)
        return hex(result_int)[2:].rjust(128, '0')


class HealthCheckInHelper(ZJULogin):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
    }

    REDIRECT_URL = "https://zjuam.zju.edu.cn/cas/login?service=https%3A%2F%2Fhealthreport.zju.edu.cn%2Fa_zju%2Fapi%2Fsso%2Findex%3Fredirect%3Dhttps%253A%252F%252Fhealthreport.zju.edu.cn%252Fncov%252Fwap%252Fdefault%252Findex%26from%3Dwap"

    @DeprecationWarning
    def get_ip_location(self):
        headers = {
            'authority': 'webapi.amap.com',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
            'sec-ch-ua-mobile': '?0',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
            'accept': '*/*',
            'sec-fetch-site': 'cross-site',
            'sec-fetch-mode': 'no-cors',
            'sec-fetch-dest': 'script',
            'referer': 'https://healthreport.zju.edu.cn/',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'cookie': 'isg=BIaGbUMSG7BxFM4x941hm4D913wI58qhRFwZi3CvdKmEcyaN2nUJsfYKT6-_W8K5',
        }

        params = (
            ('key', '729923f88542d91590470f613adb27b5'),
            ('callback', 'jsonp_859544_'),
            ('platform', 'JS'),
            ('logversion', '2.0'),
            ('appname', 'https://healthreport.zju.edu.cn/ncov/wap/default/index'),
            ('csid', '17F714D6-756D-49E4-96F2-B31F04B14A5A'),
            ('sdkversion', '1.4.16'),
        )
        response = self.sess.get(
            'https://webapi.amap.com/maps/ipLocation?key=729923f88542d91590470f613adb27b5&callback=jsonp_859544_&platform=JS&logversion=2.0&appname=https%3A%2F%2Fhealthreport.zju.edu.cn%2Fncov%2Fwap%2Fdefault%2Findex&csid=17F714D6-756D-49E4-96F2-B31F04B14A5A&sdkversion=1.4.16',
            headers=headers, params=params)
        return take_out_json(response.text)

    def get_geo_info(self, location: dict):
        params = (
            ('key', '729923f88542d91590470f613adb27b5'),
            ('s', 'rsv3'),
            ('language', 'zh_cn'),
            ('location', '{lng},{lat}'.format(lng=location.get("lng"), lat=location.get("lat"))),
            ('extensions', 'base'),
            ('callback', 'jsonp_376062_'),
            ('platform', 'JS'),
            ('logversion', '2.0'),
            ('appname', 'https://healthreport.zju.edu.cn/ncov/wap/default/index'),
            ('csid', '63157A4E-D820-44E1-B032-A77418183A4C'),
            ('sdkversion', '1.4.19'),
        )

        response = self.sess.get('https://restapi.amap.com/v3/geocode/regeo', headers=self.headers, params=params, )
        return take_out_json(response.text)

    def take_in(self, geo_info: dict, campus: str):
        formatted_address = geo_info.get("regeocode").get("formatted_address")
        address_component = geo_info.get("regeocode").get("addressComponent")
        if not formatted_address or not address_component: return

        # 获得id和uid参数-->新版接口里不需要这两个参数了
        res = self.sess.get(self.BASE_URL, headers=self.headers)
        html = res.content.decode()
        new_info_tmp = json.loads(re.findall(r'def = ({[^\n]+})', html)[0])
        # new_info_tmp = json5.loads(re.findall(r'def = (\{.*?\});', html, re.S)[0])
        # print(new_info_tmp)
        new_id = new_info_tmp['id']
        new_uid = new_info_tmp['uid']
        # 拼凑geo信息
        lng, lat = address_component.get("streetNumber").get("location").split(",")
        geo_api_info_dict = {"type": "complete", "info": "SUCCESS", "status": 1,
                             "position": {"Q": lat, "R": lng, "lng": lng, "lat": lat},
                             "message": "Get ipLocation success.Get address success.", "location_type": "ip",
                             "accuracy": 40, "isConverted": "true", "addressComponent": address_component,
                             "formattedAddress": formatted_address, "roads": [], "crosses": [], "pois": []}

        data = {
            "sfymqjczrj": "0",
            "sfyrjjh": "0",
            "nrjrq": "0",
            "sfqrxxss": "1",
            "sfqtyyqjwdg": "0",
            "sffrqjwdg": "0",
            "zgfx14rfh": "0",
            "sfyxjzxgym": "1",
            "sfbyjzrq": "5",
            "jzxgymqk": "2",
            "campus": campus,
            "ismoved": "0",
            "tw": "0",
            "sfcxtz": "0",
            "sfjcbh": "0",
            "sfcxzysx": "0",
            "sfyyjc": "0",
            "jcjgqr": "0",
            'address': formatted_address,
            'geo_api_info': geo_api_info_dict,
            'area': "{} {} {}".format(address_component.get("province"), address_component.get("city"),
                                      address_component.get("district")),
            'province': address_component.get("province"),
            'city': address_component.get("city"),
            "sfzx": "1",
            "sfjcwhry": "0",
            "sfjchbry": "0",
            "sfcyglq": "0",
            "sftjhb": "0",
            "sftjwh": "0",
            "sfyqjzgc": "0",
            "sfsqhzjkk": "1",
            "sqhzjkkys": "1",
            # 日期
            'date': get_date(),
            'created': round(time.time()),
            "szsqsfybl": "0",
            "sfygtjzzfj": "0",
            "uid": new_uid,
            "id": new_id,
            "verifyCode": cope_with_captcha(self.sess),
            "dbfb7190a31b5f8cd4a85f5a4975b89b": "1651977968",
            "1a7c5b2e52854a2480947880eabe1fe1": "a3fefb4a32d22d9a3ff5827ac60bb1b0"
        }
        response = self.sess.post('https://healthreport.zju.edu.cn/ncov/wap/default/save', data=data,
                                  headers=self.headers)
        return response.json()

    def run(self):
        print("正在为{}健康打卡".format(self.username))
        if self.delay_run:
            # 确保定时脚本执行时间不太一致
            time.sleep(random.randint(0, 360))
        # 拿到Cookies和headers
        self.login()
        # 拿取eai-sess的cookies信息
        self.sess.get(self.REDIRECT_URL)
        # 由于IP定位放到服务器上运行后会是服务器的IP定位， 因此这边手动执行后获得IP location后直接写死
        # 如果是其他校区可以在本地运行下get_ip_location()后拿到location数据写死
        # location = self.get_ip_location()
        # print(location)

        # 软院位置得到的IP定位, 如果不是软院的, 则执行上面代码后代替这边的location位置
        location = {'info': 'LOCATE_SUCCESS', 'status': 1, 'lng': '121.63529', 'lat': '29.89154'}
        geo_info = self.get_geo_info(location)
        # print(geo_info)
        try:
            res = self.take_in(geo_info, campus="宁波校区")
            print(res)
        except Exception as e:  # 失败消息推送
            push2pushplus("打卡失败, {}".format(e))


if __name__ == '__main__':
    f_name = "account.json"
    # 填写要自动打卡的：账号 密码, 然后自己实现循环即可帮多人打卡
    # aps = [("<username>", "<password>")]
    account = ""
    pwd = ""
    if account == "" or pwd == "":
        if not os.path.exists(f_name):
            with open(f_name, "w") as f:
                account, pwd = input("请输入账号, 密码：").split()
                json.dump({"account": account, "password": pwd}, f)
        else:
            f = open(f_name, "r")
            try:
                d = json.load(f)
            except json.decoder.JSONDecodeError:
                f.close()
                import os

                os.remove(f_name)
                print("删除错误Json文件")
                with open(f_name, "w") as f:
                    account, pwd = input("请输入账号, 密码：").split()
                    json.dump({"account": account, "password": pwd}, f)
            else:
                account, pwd = d.get("account"), d.get("password")

    s = HealthCheckInHelper(account, pwd, delay_run=False)
    s.run()
