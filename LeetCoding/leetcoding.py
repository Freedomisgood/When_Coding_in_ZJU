from datetime import datetime
import requests
import json
import requests
import time
import hmac
import hashlib
import base64
import urllib.parse

# coding
access_token = "7b19a779fbb6a142d275e50b09938a8413b04b5877d7a6ac8b123509ea7a5c47"
secret = 'SECb4f794d4deff54a9f22836a8d25f3f939f6f86a102a7cdda3678d47012bd9b31'
# my
# access_token = "8079a01c1d6abb49808fc0f6f4f8d2626430ca9dc9ab7208f1e96ead27346ef7"
# secret = 'SECfc01739fc6fd69a800ce4f1f1511ec09809fb2f79f1c94b280a15d36c1fd8df8'

def getTimestampSign():
    timestamp = str(round(time.time() * 1000))
    secret_enc = secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    return timestamp, sign


def getQuestion():
    base_url = 'https://leetcode-cn.com'

    # 获取今日每日一题的题名(英文)
    response = requests.post(base_url + "/graphql", json={
        "operationName": "questionOfToday",
        "variables": {},
        "query": "query questionOfToday { todayRecord {   question {     questionFrontendId     questionTitleSlug     __typename   }   lastSubmission {     id     __typename   }   date   userStatus   __typename }}"
    })
    leetcodeTitle = json.loads(response.text).get('data').get('todayRecord')[0].get("question").get('questionTitleSlug')


    # 获取今日每日一题的所有信息
    url = base_url + "/problems/" + leetcodeTitle
    url = base_url + "/problems/" + leetcodeTitle
    response = requests.post(base_url + "/graphql",
                             json={"operationName": "questionData", "variables": {"titleSlug": leetcodeTitle},
                                   "query": "query questionData($titleSlug: String!) {  question(titleSlug: $titleSlug) {    questionId    questionFrontendId    boundTopicId    title    titleSlug    content    translatedTitle    translatedContent    isPaidOnly    difficulty    likes    dislikes    isLiked    similarQuestions    contributors {      username      profileUrl      avatarUrl      __typename    }    langToValidPlayground    topicTags {      name      slug      translatedName      __typename    }    companyTagStats    codeSnippets {      lang      langSlug      code      __typename    }    stats    hints    solution {      id      canSeeDetail      __typename    }    status    sampleTestCase    metaData    judgerAvailable    judgeType    mysqlSchemas    enableRunCode    envInfo    book {      id      bookName      pressName      source      shortDescription      fullDescription      bookImgUrl      pressImgUrl      productUrl      __typename    }    isSubscribed    isDailyQuestion    dailyRecordStatus    editorType    ugcQuestionId    style    __typename  }}"})
    jsonText = json.loads(response.text).get('data').get("question")
    # 题目题号
    no = jsonText.get('questionFrontendId')
    # 题名（中文）
    leetcodeTitle = jsonText.get('translatedTitle')
    # 题目难度级别
    level = jsonText.get('difficulty')
    # 题目内容
    context = jsonText.get('translatedContent')
    url = "https://leetcode-cn.com/problems/" + "-".join(jsonText.get("title").split())
    return no, level, leetcodeTitle, context, url


def post():
    timestamp, s = getTimestampSign()
    no, level, leetcodeTitle, context, url = getQuestion()
    # data = {
    #         "msgtype": "markdown",
    #         "markdown": {
    #             "title": "Leetcode",
    #             "text": "Leetcode: [{}-{}-{}]({})".format(no, level, leetcodeTitle, url)
    #         },
    #         "at": {"isAtAll": False},
    #     }

    data =     {
    "msgtype": "actionCard",
    "actionCard": {
        "title": "Leetcode", 
        # "text": "Leetcode: [{}-{}-{}]({})".format(no, level, leetcodeTitle, url),
        "text": "Leetcode: {}-{}-{}".format(no, level, leetcodeTitle),
        "btnOrientation": "0", 
        "btns": [
            {
                "title": "查看原文", 
                "actionURL": url
            }, 
        ]
    }
}

    res = requests.post("https://oapi.dingtalk.com/robot/send?access_token={}&timestamp={}&sign={}".format(access_token, timestamp,s), 
        headers={"Content-Type": "application/json"}, data=json.dumps(data))
    print(res.text)


if __name__ == '__main__':
    post()
