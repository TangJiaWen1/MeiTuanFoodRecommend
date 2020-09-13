#导入包
from idlelib.multicall import r
import requests
import csv
import pandas as pd
import time
import random
import socket

socket.setdefaulttimeout(20)
def getview(shopid, commentcount):
    #userId=648865429
    url =r'https://www.meituan.com/meishi/api/poi/getMerchantComment?uuid=769d3436-907c-45a4-9b42-1e54778a00a6&platform=1&partner=126&originUrl=https%3A%2F%2Fwww.meituan.com%2Fmeishi%2F157361898%2F&riskLevel=1&optimusCode=10&id=' + str(
             shopid) + '&userId=648865449&offset=300&pageSize=200&sortType=1'
    headers_meituan = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate, sdch',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Cache-Control':'max-age=0',
    'DNT':'1',
    'Host':'bj.meituan.com',
    'Proxy-Connection':'keep-alive',
    'Referer':'http://bj.meituan.com/shop/286725?acm=UwunyailsW15518532529028663069.286725.1&mtt=1.index%2Fdefault%2Fpoi.pz.1.j4cijrmg&cks=58899',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}


    #创建文件夹并打开
    path = 'D:/pycharmWebCrawler/foodcomments1/'+str(shopid)+".csv"
    fp = open(path, 'a', newline='', encoding = 'utf-8-sig')
    writer = csv.writer(fp) #我要写入
    #写入内容
    writer.writerow(('用户', 'ID', 'star', 'time','comments')) #运行一次

    #7992D68BE8BC94B63A9836248DBB27674B4E29472AA8CE5B890DA41BD2054E84
    #769d3436-907c-45a4-9b42-1e54778a00a6
    #61da6d39843b4dc78f49.1587002368.1.0.0
    #8d7c0047441b44f3b88f.1586889166.1.0.0
    #28751daefffc4ba3b0cc.1587004365.1.0.0
    #d6c8026e-ccb2-46b3-8e77-1f5dad952f63

    uuid_list = ['7992D68BE8BC94B63A9836248DBB27674B4E29472AA8CE5B890DA41BD2054E84',
                 '769d3436-907c-45a4-9b42-1e54778a00a6',
                 '61da6d39843b4dc78f49.1587002368.1.0.0',
                 '8d7c0047441b44f3b88f.1586889166.1.0.0',
                 '28751daefffc4ba3b0cc.1587004365.1.0.0',
                 'd6c8026e-ccb2-46b3-8e77-1f5dad952f63',
                 '4d1bba24a81f03f25f8c.1589297614.1.0.0',
                 '7bf1a0aba0003e60b32e.1589297486.1.0.0',
                 'fcdbd434a21d71855768.1589297445.1.0.0',
                 '',
                 '',
                 '',
                 '',
                 '']
    #每一次卡顿时，人为切换一个uuid。
    for num in range(0, commentcount, 10):
        print ('正在爬取%s条…'%num)
        ajax_url = 'https://www.meituan.com/meishi/api/poi/getMerchantComment?uuid=7992D68BE8BC94B63A9836248DBB27674B4E29472AA8CE5B890DA41BD2054E84&platform=1&partner=126&originUrl=https%3A%2F%2Fwww.meituan.com%2Fmeishi%2F157361898%2F&riskLevel=1&optimusCode=10&id=' + str(
             shopid) + '&userId=&offset=' + str(num)+' \
                   ' + '&pageSize=10&sortType=1 '
        #time.sleep(random.randint(1, 5))
        #requests.adapters.DEFAULT_RETRIES=5
        try:
            reponse = requests.get(url = ajax_url, headers=headers_meituan)
            print('right response', reponse.json())
        except:
            print("Connection refused by the server..")
            print("wait sleep")
            print("sleep")
            time.sleep(5)
            print(" continue")
            continue

        for item in reponse.json()['data']['comments']:

            name = item['userName']
            user_id = item['userId']
            stars = item['star']
            comment_time = item['commentTime']
            comments = item['comment']
            result = (name, user_id,  stars, comment_time, comments)
            writer.writerow(result)
    fp.close()

if __name__ == "__main__":

    xlsx = 'all_information.xlsx'
    id_list = pd.read_excel(xlsx)['poiId']
    size_list = pd.read_excel(xlsx)['allCommentNum']
    #5.9,从11开始直接运行。
    for i in range(58, 150):
        print("i am in", i)
        getview(id_list[i], size_list[i])

