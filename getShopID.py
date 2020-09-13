import urllib.request
import csv
import urllib.error
import re
import json
import time
import pandas as pd
import socket

socket.setdefaulttimeout(20)
def obtainData(page):
    url = "https://bj.meituan.com/meishi/pn" + str(page) + "/"

    # Agent头
    Agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
    headers = {"User-Agent": Agent}
    req = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(req)
    html = str(response.read(), 'utf-8')
    pattern = re.compile(r'{"poiId":.*?}', re.S)
    item_list = pattern.findall(html)  # 获取数据
    print(item_list)
    poiId =[]
    title =[]
    avgScore =[]
    allCommentNum =[]
    address =[]
    avgPrice =[]
    for data in item_list:
        dictinfo = json.loads(data)
        print(dictinfo)
        poiId.append(dictinfo["poiId"])
        title.append(dictinfo["title"])
        avgScore.append(dictinfo["avgScore"])
        allCommentNum.append(dictinfo["allCommentNum"])
        address.append(dictinfo["address"])
        avgPrice.append(dictinfo["avgPrice"])

    return poiId,title,avgScore,allCommentNum,address,avgPrice

if __name__ == "__main__":
    all_poiId =[]
    all_title =[]
    all_avgScore =[]
    all_allCommentNum =[]
    all_address =[]
    all_avgPrice =[]
    for i in range(1, 11):
        time.sleep(3)
        print('第{i}页数据')
        poiId,title,avgScore,allCommentNum,address,avgPrice = obtainData(i)
        all_poiId.extend(poiId)
        all_title.extend(title)
        all_avgScore.extend(avgScore)
        all_allCommentNum.extend(allCommentNum)
        all_address.extend(address)
        all_avgPrice.extend(avgPrice)
    all_data = pd.DataFrame({'poiId':all_poiId, "title":all_title, "avgScore":all_avgScore,
                             "allCommentNum":all_allCommentNum, "address":all_address,"avgPrice":all_avgPrice})
    all_data.to_excel('all_information1.xlsx')

