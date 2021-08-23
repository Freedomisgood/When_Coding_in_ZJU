import re
import time

import requests
from lxml import etree

headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
}

_time = time.strftime("%Y-%m-%d", time.localtime())
# _time = "2020-09-22"


def submit_info(secret_key,info):
    requests.post(url='https://sc.ftqq.com/{}.send'.format(secret_key),data=info)

cookies = {
    'td_cookie': '36258965',
    'Hm_lvt_fe30bbc1ee45421ec1679d1b8d8f8453': '1599619275',
    'JSESSIONID': '5A6BFFC2B238F873EA2E7360308592D9',
}

headers = {
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Referer': 'http://www.cst.zju.edu.cn/32178/list2.htm',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
}

response = requests.get('http://www.cst.zju.edu.cn/32178/list1.htm', headers=headers, cookies=cookies)
response.encoding = 'utf8'
html = etree.HTML(response.text)

PREFIX_URL = "http://www.cst.zju.edu.cn/"


def getNews():
    NotesList = html.xpath('//*[@id="wp_news_w15"]/div/ul/li')
    # print("getNews", len(NotesList))

    noteTitleList = []
    wholeUrlList = []
    announceDateList = []

    for i, note in enumerate(NotesList):
        announceDate = note.xpath('span[2]/text()')[0]
        # print(announceDate)
        if announceDate == _time:
            # print(announceDate)
            announceDateList.append(announceDate)

            noteTitle = note.xpath('span[1]/a/text()')[0]
            # print(noteTitle)
            noteTitleList.append(noteTitle)
            suffixUrl = note.xpath('span[1]/a/@href')[0]
            wholeUrl = PREFIX_URL + suffixUrl
            # print(wholeUrl)
            wholeUrlList.append(wholeUrl)
    return zip(noteTitleList, wholeUrlList, announceDateList)



def analyse():
    content = getNews()
    for noteTitle, wholeUrl, announceDate in content:
        print(noteTitle, wholeUrl, announceDate)
        if wholeUrl.endswith('.htm'):
            detail = getDetailpage(wholeUrl)
            print("detail", detail)
            yield noteTitle, detail


def getDetailpage(detailUrl):
    html = requests.get(url=detailUrl,headers=headers)
    html.encoding = 'utf-8'
    content = etree.HTML(html.text)
    notes = content.xpath('/html/body/div[2]/div/div[2]/div[4]/div')[0]
    stringResult = ''
    for content in notes:
        if content.tag == 'div':        # 表
            tabletitle = content.xpath('table/tbody/tr[1]/td')  # 表格头
            # print(tabletitle)
            # 注意map被使用过(list)一次后就无效了, print(结果为空)
            tabletitleList = map(lambda x: x.xpath('string(.)'), tabletitle)
            tablehead = '|' + '|'.join(tabletitleList) + '|'  # 效果为|序号|学号|姓名|性别|学院|专业|
            tableover = '|' + ':---:|' * len(tabletitle)  # 居中显示
            tablecontent = ''
            trs = content.xpath('table/tbody/tr')
            for tr in trs[1:]:                                 #多行row
                tds = map(lambda x: x.xpath('string(.)'), tr)  # 一行内容
                tablecontent += '|' + '|'.join(tds) + '|' + '\n'
            tableinfo = tablehead + '\n' + tableover + '\n' + tablecontent
            stringResult += '\n' + tableinfo + '\n'# 将表格分离开一点
        elif content.tag == 'p':
            Pcontent = content.xpath('string(.)')
            if re.match('["一二三四五六七八九十"]+、', Pcontent):
                stringResult += "####" + Pcontent + '\n\n'
            elif re.match('\d+.', Pcontent):
                stringResult += "#####" + Pcontent + '\n\n'
            else:
                stringResult += content.xpath('string(.)') + '\n\n'
        else:
            print("未知格式")
    return stringResult


if __name__ == "__main__":
    keyList = {
        'cl':'SCU35113Te369cebc21f6e483c03fffc400c4c5c05bdad63995c32',
    }

    for info in analyse():
        title, detail = info
        print(info)
        data_info = {
            'text': '【招生信息】' + title,
            'desp': detail
        }
        # print("发送的是:", title)
        for secret_key in keyList.values():
            submit_info(secret_key, data_info)
            print("发送成功")
