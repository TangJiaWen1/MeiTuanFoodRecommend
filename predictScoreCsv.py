import csv
from pandas import read_excel
from sklearn.model_selection import KFold
import numpy as np
import random
from sklearn.utils import shuffle
from sklearn.model_selection import KFold
import xlrd
import pandas as pd
import os



'''
#将dataframe转换为txt
df.to_csv('output.txt', sep='\t', index=0, header=0)

'''


# 将txt格式的数据转换为libvsm格式文件。
def CSVtoLibsvm(datapath, savepath):
    # read data file
    readin = open(datapath, 'r')
    # write data file
    output = open(savepath, 'w')
    try:
        the_line = readin.readline()
        while the_line:
            # delete the \n
            the_line = the_line.strip('\n')
            index = 0;
            output_line = ''
            for sub_line in the_line.split('\t'):
                # the label col
                if index == 0:
                    output_line = sub_line
                # the features cols
                if sub_line != 'NULL' and index != 0:
                    the_text = ' ' + str(index) + ':' + sub_line
                    output_line = output_line + the_text
                index = index + 1
            output_line = output_line + '\n'
            output.write(output_line)
            the_line = readin.readline()
    finally:
        readin.close()

def getVipid():
    #获取店铺名列表。
    vip_list =[]
    for info in os.listdir('D:/pycharmWebCrawler/vipComments'):
        userid = info[:-4]
        vip_list.append(userid)
    print(vip_list)
    return vip_list


if __name__ == "__main__":
    #viplist =getVipid()
    # for user in viplist:
    #     domain = os.path.abspath(r'D:/pycharmWebCrawler/vipComments')  # 获取文件夹的路径
    #     csv_path = os.path.join(domain, str(user) + ".csv")  # 将路径与文件名结合起来就是每个文件的完整路径  
    #     # print('csvpath', csv_path)
    #     sav_path = os.path.join(domain, str(user) + ".csv")
    #     try:
    #         data =pd.read_csv(csv_path)
    #         predict_df = data[['star','clean','sever','food']]
    #         predict_df.to_csv("D:/pycharmWebCrawler/viplibTxt/vip_{}.txt".format(user), sep="\t", index=False, header=None)
    #         CSVtoLibsvm("D:/pycharmWebCrawler/viplibTxt/vip_{}.txt".format(user), "D:/pycharmWebCrawler/viplibTxt/libtrian_{}.txt".format(user))
    #
    #     except pd.errors.EmptyDataError:
    #
    #         print("空文件，跳过")
    #         pass
    #
    # data = pd.read_csv('D:/pycharmWebCrawler/vip _test.csv')
    # predict_df = data[['star','clean','sever','food']]
    # predict_df.to_csv("D:/pycharmWebCrawler/viplibTxt/viptest_{}.txt".format(11), sep="\t", index=False, header=None)
    # CSVtoLibsvm("D:/pycharmWebCrawler/viplibTxt/viptest_{}.txt".format(11), "D:/pycharmWebCrawler/viplibTxt/libvipTest_{}.txt".format(11))

    viplist = getVipid()
    df = pd.DataFrame(columns=viplist)
    df.to_csv('D:/pycharmWebCrawler/vipname.csv',sep="\t", index=False)



