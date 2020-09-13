import os
from collections import defaultdict
import re
import zhon.hanzi
from snownlp import SnowNLP
from math import isnan
import pandas as pd
import numpy as np

shopid_list = []
# 版本为python3，如果为python2需要在字符串前面加上u

def cut_sent(para):
    #对中文分句进行切分。
    para = re.sub('([。，！？\?])([^”’])', r"\1\n\2", para)  # 单字符断句符
    para = re.sub('(\.{6})([^”’])', r"\1\n\2", para)  # 英文省略号
    para = re.sub('(\…{2})([^”’])', r"\1\n\2", para)  # 中文省略号
    para = re.sub('([。！？\?][”’])([^，。！？\?])', r'\1\n\2', para)
    # 如果双引号前有终止符，那么双引号才是句子的终点，把分句符\n放到双引号后，注意前面的几句都小心保留了双引号
    para = para.rstrip()  # 段尾如果有多余的\n就去掉它
    # 很多规则中会考虑分号;，但是这里我把它忽略不计，破折号、英文双引号等同样忽略，需要的再做些简单调整即可。
    return para.split("\n")

def getShopid():
    #获取店铺名列表。
    shopid_list =[]
    for info in os.listdir('D:/pycharmWebCrawler/foodcomments'):
        shopid = info[:-4]
        shopid_list.append(shopid)
    print(shopid_list)
    return shopid_list

def judge_null(column):
    if pd.isnull(column):
        return None
    return column

def getVipcomment(dataf):
    f = open("user_vip.txt", "r")
    user_vip = f.readlines()
    vip_str = user_vip[0]
    vip_list = eval(vip_str)
    print(vip_list)
    f.close()

    #获取vip用户列表
    vip_df = dataf
    #获取每一个user将要填充的dataframe模板。
    shopid_list = getShopid()
    #获取所有的shopid，从而方面每一个user去遍历。


    # 得到useridlist
    for user in (vip_list):
        for shopid in shopid_list:
            domain = os.path.abspath(r'D:/pycharmWebCrawler/foodcomments')  # 获取文件夹的路径
            csv_path = os.path.join(domain, str(shopid) + ".csv")  # 将路径与文件名结合起来就是每个文件的完整路径  
            #print('csvpath', csv_path)
            try:
                data = pd.read_csv(csv_path)
                dd = data[(data['ID'] == user)]
                dd['comments'] = dd.apply(lambda row: judge_null(row['comments']), axis=1)
                if dd.empty:
                    continue
                else:

                    for index, row in dd.iterrows():
                        comment_str = row['comments']
                        print('comments', comment_str)
                        if comment_str == None:
                            print('i am here')
                            continue

                        s = SnowNLP(comment_str)
                        s.words
                        s.tags
                        avg_score = (s.sentiments*100)
                        print('avg avg avg score', avg_score)
                        split_lst = cut_sent(comment_str)
                        clean_score = getCleanpoint(split_lst, avg_score)
                        serve_score = getServepoint(split_lst, avg_score)
                        food_score = getFoodpoint(split_lst, avg_score)
                        vip_df = vip_df.append([{'ID': user, 'star': row['star'], 'clean':clean_score, 'sever':serve_score, 'food': food_score}], ignore_index=True)
            except pd.errors.EmptyDataError:

                print("空文件，跳过")
                pass
        vip_df = vip_df.drop_duplicates(subset=['ID',    'clean',  'sever', 'food'], keep='first')
        print(vip_df)
        path = 'D:/pycharmWebCrawler/vipComments/' + str(user) + ".csv"
        vip_df.to_csv(path)
        vip_df.drop(vip_df.index, inplace=True)




def getCleanpoint(str_list,avg_score):
    envir_list = ['环境', '卫生', '干净', '脏']
    count = 0
    grade = 0
    for i in str_list:
        for j in envir_list:
            if i.find(j) ==-1:
                pass
            else:
                #print("Found  in the string.")
                count = count +1
                #print(i)
                c_str = SnowNLP(i)
                c_str.words
                c_str.tags
                grade = grade+c_str.sentiments*100
                break
    if count ==0:
        print('avg  avg',avg_score)
        return avg_score
    else:
        print(1)
        print('grade', grade)
        print('count', count)
        print('score', grade/count)
        return grade/count

def getServepoint(str_list,avg_score):
    envir_list = ['服务','态度','脸色','店员']
    count = 0
    grade = 0
    for i in str_list:
        for j in envir_list:
            if i.find(j) ==-1:
               pass

            else:
                print("Found  in the string.")
                count = count +1
                print(i)
                c_str = SnowNLP(i)
                c_str.words
                c_str.tags
                grade = grade+c_str.sentiments*100
                break
    if count ==0:
        print('avg  avg', avg_score)
        return avg_score
    else:
        print(1)
        print('grade', grade)
        print('count', count)
        print('score', grade / count)
        return grade/count

def getFoodpoint(str_list,avg_score):
    envir_list = ['菜', '吃', '食', '味', '果']
    count = 0
    grade = 0
    for i in str_list:
        for j in envir_list:
            if i.find(j) ==-1:
                pass
            else:
                print("Found  in the string.")
                count = count +1
                print(i)
                c_str = SnowNLP(i)
                c_str.words
                c_str.tags
                grade = grade+c_str.sentiments*100
                break
    if count == 0:
        print('avg  avg', avg_score)
        return avg_score
    else:
        print(1)
        print('grade', grade)
        print('count', count)
        print('score', grade / count)
        return grade/count

def getShopAvg(total_df):
    '''''
    传入dataframe格式
    里面的star设为0，为预测值。
    ID 为userid
    同时按照时间排序，获得前100个评论。

    '''
    shopid_list = getShopid()
    shop_df = total_df
    for shopid in shopid_list:
        domain = os.path.abspath(r'D:/pycharmWebCrawler/foodcomments')  # 获取文件夹的路径
        csv_path = os.path.join(domain, str(shopid) + ".csv")  # 将路径与文件名结合起来就是每个文件的完整路径  
        CommentList = []
        count = 0 #计数器，最大为200
        try:
            data = pd.read_csv(csv_path)
            #print(data)
            data.sort_values('time', inplace=True)
            #print(data)
            data['comments'] = data.apply(lambda row: judge_null(row['comments']), axis=1)
            for index, row in data.iterrows():
                if count >100:
                    break
                comment_str = row['comments']
                try:
                    split_lst = cut_sent(comment_str)
                    CommentList.extend(split_lst)
                except :
                    pass
                count = count+1
                if comment_str == None:
                    print('i am here')
                    continue


            avg_score = 50
            print('avg avg avg score', avg_score)

            clean_score = getCleanpoint(CommentList, avg_score)
            serve_score = getServepoint(CommentList, avg_score)
            food_score = getFoodpoint(CommentList, avg_score)
            shop_df = shop_df.append([{'ID': shopid, 'star': 0, 'clean': clean_score, 'sever': serve_score, 'food': food_score}], ignore_index=True)

        except pd.errors.EmptyDataError:

            print("空文件，跳过")
            pass
    shop_df.to_csv('vip _test.csv')

if __name__ == "__main__":
   total_df = pd.DataFrame(columns=['ID', 'star', 'clean', 'sever', 'food'])
   #getVipcomment(total_df)
   getShopAvg(total_df)

   #comment_str ='下午来的，错过饭点，住邦2000的店，客人很少，不过只有一个店员，稍等了一下就好了，验证很快，出餐速度也很快，选的金枪鱼三文治，味道没觉得有多大区别，都是一样的，饮料选的红茶就是茶包，简单喝点还是不错的，可以推荐'







