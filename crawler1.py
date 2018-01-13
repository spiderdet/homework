# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
from datetime import datetime
import urllib2, re, urlparse, os, urllib, sys, time, random

def valid_filename(s):    #将域名最后的数字作为文件名
                          #如http://www.douguo.com/cookbook/1642994.html 为 1642994
    s = s.split('/')[-1]
    s = s.split('.')[0]
    return s

def get_all_links(content): #找到此页面上所有的同类菜谱链接
    links = []
    bsobj = BeautifulSoup(content, "html.parser", from_encoding="gbk")
    nextpages = bsobj.findAll('a', {'href': re.compile('http://www\.douguo\.com/cookbook/\d+\.html')})
    for page in nextpages:
        page1 = page.attrs['href']
        links.append(page1)
    return links

def union_bfs(a, b):   #使用bfs方法爬取
    for e in b:
        if e not in a:
            a.insert(0, e)

def add_page_to_folder(page, content): #将页面中需求的内容存入文件夹

    folder = 'html'  # 存放网页的文件夹
    filename = valid_filename(page)  # 将网址变成合法的文件名
    if not os.path.exists(folder):  # 如果文件夹不存在则新建
        os.mkdir(folder)
    if os.path.exists(os.path.join(folder, filename)):
        print('yes, ' + filename +' exists..')
        return 1

    else:
        f = open(os.path.join(folder, filename), 'w')
        page = page.encode('ascii', 'ignore')
        f.write(page + '\n')  # 将网页存入文件, 改变了之前保存整个网页的方法, 节省空间

        bsobj = BeautifulSoup(content, "html.parser", from_encoding="gbk")
        obj = bsobj.find('div', {'class': "recinfo"})  # name 菜名
        name = obj.h1.get_text().strip()
        #print('name : ' + name)
        f.write(name + '\n')

        obj = bsobj.find('div', {'class': "falisc"})  # collect number 收藏数
        obj = obj.find('span', {'class': 'collectnum'})
        collectnum = obj.get_text().strip()
        #print('collect_num : ' + collectnum)
        f.write(collectnum + '\n')

        obj = bsobj.find('div', {'class': "recinfo"})  # img url 图片地址
        img_url = obj.find('a').attrs['href']
        #print('img_url : ' + img_url)
        f.write(img_url + '\n')

        obj = bsobj.find('table', {'class': "retamr"})  # zhuliao  主料
        obj = obj.findAll('tr', class_="mtim")
        if 'class' in obj[0].td.attrs:  #若第一个tr为难度,预计时间的抬头
            zliao = obj[1]  #主料为第二个tr
        else:
            zliao = obj[0] #否则主料就是第一个tr
        zhuliao = ''
        i = zliao
        while (i.find_next('tr') != None):
            i = i.find_next('tr')
            if 'class' in i.attrs:  # 若进入辅料tr, 则退出, 保证只搜到主料
                break
            zhuliao = zhuliao + i.td.span.get_text().strip() + ' '
            if i.td.find_next('td').span != None:
                zhuliao = zhuliao + i.td.find_next('td').span.get_text().strip() + ' '
        #print('zhuliao : ' + zhuliao)
        f.write(zhuliao + '\n')

        obj = bsobj.find('div', {'class': "step clearfix"})  # zuofa 做法
        result = obj.findAll('p')
        zuofa, line = '', ''
        for i in result:
            line = i.get_text().strip()
            zuofa = zuofa + line + '\t'
        #print('zuofa : ' + zuofa)
        #print('\n\n')
        f.write(zuofa + '\n')

        f.close()
        return 0

def save(count, tocrawl, crawled):  #保存tocrawl和crawled列表于txt文件
    print('Has crawled ', count, ' pages')
    print('Saving process proceeding..')
    file1 = open('tocrawl.txt', 'w')
    file2 = open('crawled.txt', 'w')
    for i in tocrawl:
        file1.write(i + '\n')
    for i in crawled:
        file2.write(i + '\n')
    file1.close()
    file2.close()
    print('Saving process completed')


def crawl1(seed, max_page, ifpass):
    tocrawl = [seed]
    crawled = []
    count = 0

    while tocrawl:
        page = tocrawl.pop()
        if page not in crawled:
            print(page)
            try:
                time.sleep(random.uniform(3, 5)) #合理访问服务器,也为可能有的反爬虫
                try:
                    content = urllib2.urlopen(page, timeout=10).read()
                except:
                    print("time out or can't open the website.")
                    crawled.append(page)
                    raise NameError       #给上一级try报错
                    continue
                flag = add_page_to_folder(page, content) #flag为1说明已爬取并保存该网页
                if flag == 0:
                    outlinks = get_all_links(content)
                    union_bfs(tocrawl, outlinks)
                    count += 1
                crawled.append(page)
                if (count >= max_page):
                    break
            except:
                print("some problems occur while crawling")
                print('the page is :' + page)
                if ifpass == 0 : #ifpass为0代表 遇错就保存进度并退出, 为1代表忽略该网页并继续
                    save(count,tocrawl, crawled)
                    exit()

    save(count,tocrawl, crawled) # 若已爬完或达到需求的爬取数目, 保存进度,以备还需要继续爬
    return


if __name__ == '__main__':
    seed = 'http://www.douguo.com/cookbook/1642994.html' #随意选了一菜谱网页作为起始
    max_page = 10000

    reload(sys)
    sys.setdefaultencoding('utf-8')

    ifpass = 1    #1代表遇错忽略该网页并继续进程, 0代表保存进度并退出
    start = datetime.now()
    crawl1(seed, max_page, ifpass)
    end = datetime.now()
    print (end - start)