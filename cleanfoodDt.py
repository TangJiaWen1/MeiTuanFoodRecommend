import os

from collections import Counter  # 引入Counter
import pandas as pd
import numpy as np
def dataToCsv(file, data):
    data = list(data)
    file_data = pd.DataFrame(data=None, index=data, columns=None, dtype=None, copy=False)

    file_data.to_csv(file)

def clean():
    shopid_list =[]
    usertotalid_list = []#所有的用户
    for info in os.listdir('D:/pycharmWebCrawler/foodcomments'):
        shopid = info[:-4]
        shopid_list.append(shopid)
        # b遍历每一个shopid，同时利用i可以知道插入行是放几个0
    shopidlist_len = len(shopid_list)
    print('shoplist_len', shopidlist_len)

    #得到useridlist
    for i in range(shopidlist_len):
        domain = os.path.abspath(r'D:/pycharmWebCrawler/foodcomments')  # 获取文件夹的路径
        csv_path = os.path.join(domain, str(shopid_list[i]) + ".csv")  # 将路径与文件名结合起来就是每个文件的完整路径  
        print('csvpath', csv_path)

        try:
            data = pd.read_csv(csv_path)
            userid_list = data['ID']
            star_list = data['star']
            usertotalid_list.extend(userid_list)

            stardict = dict(zip(userid_list, star_list))
            print(stardict)
            f = open('D:/pycharmWebCrawler/foodcommentsDict/'+shopid_list[i]+'dict.txt', 'w')
            f.write(str(stardict))
            f.close()


        except pd.errors.EmptyDataError:
            stardict = dict()
            f = open('D:/pycharmWebCrawler/foodcommentsDict/' + shopid_list[i] + 'dict.txt', 'w')
            f.write(str(stardict))
            f.close()
            print("空文件，跳过")
            pass

    print('user len',len(usertotalid_list))#user len 83629
    l2 = []
    b = dict(Counter(usertotalid_list))
    print('b len',len(b))
    l2 =[key for key, value in b.items() if value > 6]
    print(l2)  # 只展示重复元素
    print({key: value for key, value in b.items() if value > 6})  # 展现重复元素和重复次数
    l2.remove('0')#删除匿名用户
    l2.remove(0)
    f = open("user_common.txt", "w")
    f.write(str(l2))
    f.close()
    print('size', len(l2))#size 14949



    score_matrix =np.matrix([shopid_list])
    print('score_matrix', score_matrix.shape)

    #遍历每一个userlist中的每一个user，对每一个user遍历所有的评价表，得到评分列表
    for item in l2:
        #print('item ', item)
        user_star_list = []
        for i in range(shopidlist_len):
            #flag = 0
            #print(" i am in ",shopid_list[i])
            f = open('D:/pycharmWebCrawler/foodcommentsDict/'+shopid_list[i]+'dict.txt', 'r')
            a = f.read()
            star_dict = eval(a)
            try:
                if item in star_dict:
                    #print(str(star_dict[item]))
                    user_star_list.append(str(star_dict[item]))
                    #print(user_star_list)
                else:
                    user_star_list.append('0')
                f.close()
            except pd.errors.EmptyDataError:
                print("空文件，跳过")
                user_star_list.append('0')
                f.close()
                pass
        #print('i am in shop_'+shopid_list[i], user_star_list)
        #print('size', len(user_star_list))
        score_matrix = np.row_stack((score_matrix, user_star_list))
        #print(score_matrix)
    np.savetxt('foo1.csv',score_matrix, delimiter=',', fmt='%s')

    f = open('D:/pycharmWebCrawler/foodcommentsDict/score_matrix.txt', 'w')
    f.write(str(score_matrix))
    f.close()
    #np.savetxt('score_matrix.csv', score_matrix, fmt='%.18e')


def createDF():

    for info in os.listdir('D:/pycharmWebCrawler/foodcomments'):
        shopid = info[:-5]
        print(shopid)


if __name__ == "__main__":
   clean()

