#!/usr/bin/python
# -*- coding:utf-8 -*-
import requests
#import sys

#reload(sys)
#sys.setdefaultencoding('utf-8')
imgfile=open('img.txt','r')
list_of_line=imgfile.readlines()
num=0
titlelist={}
for i in list_of_line:
    num+=1
    i=i.split('\t')
    title=i[0]
    print("正在保存图片"+title)
    try:
        img=requests.get(i[1][:-1]).content
	
    except:
        print("获取图片失败")
    else:
     	title = title.replace('/','########')
        if(title in titlelist):
            titlelist[title]+=1
            if(i[1][-3]=='n'):
                f = open('dataset//' + title + '(' + str(titlelist[title]) + ')' + '.png', 'ab')
            else:
                f=open('dataset//' + title + '('+str(titlelist[title])+')'+'.jpg', 'ab')
            f.write(img)
            f.close()
        else:
            titlelist[title]=1
            if (i[1][-3] == 'n'):
                f = open('dataset//' + title + '.png', 'ab')
            else:
                f = open("dataset//" + title + '.jpg', 'ab')
            f.write(img)
            f.close()
        print("该图片保存完毕")
