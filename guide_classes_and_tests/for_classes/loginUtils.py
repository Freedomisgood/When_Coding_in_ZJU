import requests
import re
import time
import urllib.parse as urlparse


# Exceptions
class LoginError(Exception):
    """Login Exception"""
    pass


class ZJULogin(object):
    """
    统一认证平台的登录使用的ZJU-nCov-Hitcarder的开源代码，感谢这位同学开源对RSA加密的贡献
    Attributes:
        username: (str) 浙大统一认证平台用户名（一般为学号）
        password: (str) 浙大统一认证平台密码
        login_url: (str) 登录url
        sess: (requests.Session) 统一的session管理
    """

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.login_url = "https://zjuam.zju.edu.cn/cas/login?service=http%3A%2F%2Fservice.zju.edu.cn%2F"
        self.sess = requests.Session()

    def login(self):
        """Login to ZJU platform"""
        res = self.sess.get(self.login_url)
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
        res = self.sess.post(url=self.login_url, data=data)
        # check if login successfully
        if '统一身份认证' in res.content.decode():
            raise LoginError('登录失败，请核实账号密码重新登录')
        print("统一认证平台登录成功")
        return self.sess

    def _rsa_encrypt(self, password_str, e_str, M_str):
        password_bytes = bytes(password_str, 'ascii')
        password_int = int.from_bytes(password_bytes, 'big')
        e_int = int(e_str, 16)
        M_int = int(M_str, 16)
        result_int = pow(password_int, e_int, M_int)
        return hex(result_int)[2:].rjust(128, '0')


class SSOLogin(ZJULogin):
    """
    完成测试需要获得token
    """
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


if __name__ == "__main__":
    login = ZJULogin(username="*", password="*")
    print("登录到浙大统一身份认证平台...")
    res = login.login()
    print(res.headers)
    print(res.cookies)
