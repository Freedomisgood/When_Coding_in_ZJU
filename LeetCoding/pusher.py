# -*- coding: utf-8 -*-
# @Time    : 2022/5/10 19:26
# @Author  : Mrli
# @File    : pusher.py

import base64
import hashlib
import hmac
import os
import time
import urllib.parse
from datetime import date
from enum import IntEnum
from functools import reduce

import requests


class PushTypeEnum(IntEnum):
    PushplusPush = 1
    DingDingPush = 2
    ServerChanPush = 3


class IPushUtil:
    def push(self, title: str = "", content: str = "", *args, **kwargs) -> bool:
        pass

    @classmethod
    def valid(cls):
        pass


class PushplusPush(IPushUtil):
    PUSHPLUS_TOKEN = os.getenv("PUSHPLUS_TOKEN", None)

    def push(self, title: str = "", content: str = "", *args, **kwargs) -> bool:
        d = {
            "token": self.PUSHPLUS_TOKEN,
            "template": "markdown",
            "title": "{date}-{title}".format(date=date.today(), title=title),
            "content": content
        }
        res = requests.post("http://www.pushplus.plus/send", data=d)
        if not (200 <= res.json().get("code") < 300):
            print(res.json())
        return 200 <= res.json().get("code") < 300

    @classmethod
    def valid(cls):
        return cls.PUSHPLUS_TOKEN is not None


class ServerChanPush(IPushUtil):
    SERVERCHAN_TOKEN = os.getenv("SERVERCHAN_TOKEN", None)

    def push(self, title: str = "", content: str = "", *args, **kwargs) -> bool:
        data = {
            'text': "{date}-{title}".format(date=date.today(), title=title),
            'desp': content
        }
        res = requests.post(url='https://sc.ftqq.com/{}.send'.format(self.SERVERCHAN_TOKEN), data=data)
        if not (res.json().get("errmsg") == "success"):
            print(res.json())
        return res.json().get("errmsg") == "success"

    @classmethod
    def valid(cls):
        return cls.SERVERCHAN_TOKEN is not None


class DingDingPush(IPushUtil):
    URL = "https://oapi.dingtalk.com/robot/send"
    # 钉钉机器人的设置
    DING_ACCESS_TOKEN = os.getenv("DING_ACCESS_TOKEN", None)
    DING_SECRET = os.getenv("DING_SECRET", None)

    def __init__(self):
        self.target_url = self.get_url()

    def get_url(self):
        timestamp = round(time.time() * 1000)
        secret_enc = bytes(self.DING_SECRET, encoding="utf-8")
        string_to_sign = "{}\n{}".format(timestamp, self.DING_SECRET)
        string_to_sign_enc = bytes(string_to_sign, encoding="utf-8")
        hmac_code = hmac.new(
            secret_enc, string_to_sign_enc, digestmod=hashlib.sha256
        ).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
        return self.URL + "?access_token={access_token}&timestamp={timestamp}&sign={sign}".format(
            access_token=self.DING_ACCESS_TOKEN, timestamp=timestamp, sign=sign)

    def push(self, title: str = "", content: str = "", *args, **kwargs) -> bool:
        # msg = self.gen_markdown_msg(title, content)
        msg = self.gen_card_msg(title, **kwargs)
        return self.send(msg)

    @classmethod
    def valid(cls):
        return cls.DING_ACCESS_TOKEN is not None and cls.DING_SECRET is not None

    def send(self, message):
        resp = requests.post(self.target_url, json=message)
        return resp.json()

    @staticmethod
    def gen_card_msg(title, *args, **kwargs):
        return {
            "msgtype": "actionCard",
            "actionCard": {
                "title": "Leetcode",
                "text": title,
                "btnOrientation": "0",
                "btns": [
                    {
                        "title": "查看原文",
                        "actionURL": kwargs.get("url")
                    },
                ]
            }
        }

    @staticmethod
    def gen_text_msg(content, at=None, at_all=False):
        if at is None:
            at = []
        return {
            "msgtype": "text",
            "text": {"content": content},
            "at": {"atMobiles": at, "isAtAll": at_all},
        }

    @staticmethod
    def gen_markdown_msg(title, text, at=None, at_all=False):
        if at is None:
            at = ["15061873738"]

        def generateText():
            res = ""
            # 最顶行显示标题
            res += "# " + title + "\n"
            # 内容
            res += text
            # at对象
            res += reduce(lambda x, y: x + "@" + y, at, "")
            return res

        return {
            "msgtype": "markdown",
            "markdown": {
                "title": title,
                "text": generateText()
            },
            "at": {"atMobiles": at, "isAtAll": at_all},
        }


class PushUtilContext:
    def __init__(self, push_type: PushTypeEnum = None):
        if not push_type:
            self.pusher = None
            self.init()
        else:
            if push_type == PushTypeEnum.PushplusPush:
                self.pusher = PushplusPush()
            elif push_type == PushTypeEnum.DingDingPush:
                self.pusher = DingDingPush()
            elif push_type == PushTypeEnum.ServerChanPush:
                self.pusher = ServerChanPush()
            else:
                raise Exception("初始化的PusherTpye不合规")

    def init(self):
        if DingDingPush.valid():
            self.pusher = DingDingPush()
        elif PushplusPush.valid():
            self.pusher = PushplusPush()
        elif ServerChanPush.valid():
            self.pusher = ServerChanPush()
        else:
            raise Exception("没有可用的Pusher, 请进行正确的配置")

    def push(self, title: str = "", content: str = "", *args, **kwargs) -> bool:
        if not self.pusher:
            print("pusher未配置或是配置错误")
            return False
        return self.pusher.push(title, content, *args, **kwargs)


# 如果要使用pusher, 则自定义
p = PushUtilContext()
