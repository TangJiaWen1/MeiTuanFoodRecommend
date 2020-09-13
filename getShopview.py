# encoding=utf-8
# import os
# os.environ['CUDA_VISIBLE_DEVICES'] = '2'
import pandas as pd
import urllib.request
import json
import time
import random
from multiprocessing import Pool
import socket

socket.setdefaulttimeout(20)


class GetInformation:
    def __init__(self, xlsx):
        self.id_list = pd.read_excel(xlsx)['poiId']

    def start_crawer(self,threshold= 149):
        Agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
        headers = {"User-Agent": Agent}
        num = 1
        comments_ = []
        stars = []
        commentTimes = []
        userIds = []
        for id in self.id_list:
            if num == threshold:
                break
            #url = r'https://www.meituan.com/meishi/api/poi/getMerchantComment?uuid=769d3436-907c-45a4-9b42-1e54778a00a6&platform=1&partner=126&originUrl=https%3A%2F%2Fwww.meituan.com%2Fmeishi%2F157361898%2F&riskLevel=1&optimusCode=10&id=' + str(
            # id) + '&userId=648865429&offset=300&pageSize=200&sortType=1'

            url = 'http://www.meituan.com/meishi/api/poi/getMerchantComment?uuid=095e5a{}d417a92d9.1526123380.1.0.0&platform=1&partner=126&originUrl=http%3A%2F%2Fwww.meituan.com%2Fmeishi%2F4955158%2F&riskLevel=1&optimusCode=1&id=' + str(
                id) + '&userId=648865429&offset=300&pageSize=200&sortType=1'.format(
                random.randint(10000, 99999))
            req = urllib.request.Request(url, headers=headers)
            response = urllib.request.urlopen(req)
            html = str(response.read(), 'utf-8')
            context = json.loads(html)
            print(context)
            comments = context['data']['comments']
            try:
                length = len(comments)
                for i in range(length):
                    stars.append(comments[i]['star'])
                    #comments_.append(comments[i]['comment'])
                    commentTimes.append(comments[i]['commentTime'])
                    userIds.append(comments[i]['userId'])
                    #print(comments[i]['comment'])
            except:
                print("Connection refused by the server..")
                print("Let me sleep for 5 seconds")
                print("ZZzzzz...")
                time.sleep(5)
                print("Was a nice sleep, now let me continue...")
                continue
            #response.close()
            time.sleep(random.randint(1, 5))
            num += 1
        get_information = pd.DataFrame(
            {'stars': stars, 'commentTimes': commentTimes, 'userIds': userIds})
        get_information.to_excel('get_information_1.xlsx')
        time.sleep(2)


if __name__ == "__main__":
    xlsx = 'all_information.xlsx'
    c = GetInformation(xlsx)
    pool = Pool(3)
    pool.apply_async(func=c.start_crawer(), args=(100))
    pool.close()
    pool.join()
