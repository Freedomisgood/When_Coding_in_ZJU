import json
import os

import requests


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


def run():
    """获取每日一题, 并推送"""
    no, level, leetcodeTitle, context, url = getQuestion()
    try:
        p = getattr(__import__("pusher"), "p")
    except AttributeError:
        # 未配置pusher
        print("未启用pusher, 请在pusher.py中打开注释启用, 并配置使用")
        # post(no, level, leetcodeTitle, context, url)
    else:
        print("采用Pusher")
        print(p.push(title="Leetcode: {}-{}-{}".format(no, level, leetcodeTitle),
                     content="Urls: {}\n\n文本内容: \n\n{}".format(url, context),
                     url=url
                     ))


if __name__ == '__main__':
    run()
