#!/usr/bin/env python
import web
from colordescriptor import ColorDescriptor
from searcher import Searcher
import cv2
from web import form
from BeautifulSoup import BeautifulSoup
import urllib2
import sys, os, lucene
from java.io import File
from java.io import StringReader
from org.apache.lucene.analysis.core import WhitespaceAnalyzer
from org.apache.lucene.analysis import TokenStream
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.util import Version
from org.apache.lucene.search.highlight import Highlighter
from org.apache.lucene.search.highlight import QueryScorer
from org.apache.lucene.search.highlight import SimpleHTMLFormatter
from org.apache.lucene.search.highlight import InvalidTokenOffsetsException
urls = (
    '/', 'index',
    '/s', 's',
    '/cm','index2',
    '/c','c',
    '/im','index_img',	
    '/i','i',
)

render = web.template.render('templates1') 

login = form.Form(
    form.Textbox('Key'),
    form.Button('Go for It'),
)

def func(command):
    STORE_DIR = "index1"
    vm_env = lucene.getVMEnv()
    vm_env.attachCurrentThread()
    directory = SimpleFSDirectory(File(STORE_DIR))
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = WhitespaceAnalyzer(Version.LUCENE_CURRENT)
    res=[]
    if command == '':
        return
    query = QueryParser(Version.LUCENE_CURRENT, "name", analyzer).parse(command)
    scoreDocs = searcher.search(query, 9).scoreDocs
    for scoreDoc in scoreDocs:
        doc = searcher.doc(scoreDoc.doc)
        try:
        	res.append([doc.get("name"), doc.get("collect_num"), doc.get("zhuliao").split(' '), doc.get("zuofa").split('\n'), doc.get("img_url"), doc.get("url")])
        except:
            pass
    res1=[]
    for i in res:
        i[1]=int(i[1])
        res1.append(tuple(i))
    res2=sorted(res1,cmp=None, key=lambda x:x[1],reverse=True)
    return res2


def func2(command):
    STORE_DIR = "index1"
    vm_env = lucene.getVMEnv()
    vm_env.attachCurrentThread()
    directory = SimpleFSDirectory(File(STORE_DIR))
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = WhitespaceAnalyzer(Version.LUCENE_CURRENT)
    res=[]
    if command == '':
        return
    query = QueryParser(Version.LUCENE_CURRENT, "zhuliao",analyzer).parse(command)
    scoreDocs = searcher.search(query, 9).scoreDocs
    for scoreDoc in scoreDocs:
        doc = searcher.doc(scoreDoc.doc)
        try:
            res.append([doc.get("name"), doc.get("collect_num"), doc.get("zhuliao").split(' '), doc.get("zuofa").split('\n'), doc.get("img_url"), doc.get("url")])
        except:
            pass
    res1=[]
    for i in res:
        i[1]=int(i[1])
        res1.append(tuple(i))
    res2=sorted(res1,cmp=None, key=lambda x:x[1],reverse=True)
    return res2	


def func3(command):
    findresult=[]
    cd = ColorDescriptor((8, 12, 3))
    query = cv2.imread(command)
    features = cd.descriptor(query)
    searcher1 = Searcher("index.csv")
    results = searcher1.search(features)
    for (score, resultID) in results:
        findresult.append(resultID[:-4])

    STORE_DIR = "index1"
    vm_env = lucene.getVMEnv()
    vm_env.attachCurrentThread()
    directory = SimpleFSDirectory(File(STORE_DIR))
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = WhitespaceAnalyzer(Version.LUCENE_CURRENT)
    res=[]
    for imgID in findresult:
        if imgID == '':
            return
        query = QueryParser(Version.LUCENE_CURRENT, "name", analyzer).parse(imgID)
        scoreDocs = searcher.search(query, 9).scoreDocs
        for scoreDoc in scoreDocs:
            doc = searcher.doc(scoreDoc.doc)
            try:
        	    res.append([doc.get("name"), doc.get("collect_num"), doc.get("zhuliao").split(' '), doc.get("zuofa").split('\n'), doc.get("img_url"), doc.get("url")])
            except:
                pass
    return res


class index:
    def GET(self):
        f = login()
        return render.search1(f)
class index2:
    def GET(self):
        f = login()
        return render.search2(f)
class index_img:
    def GET(self):
        f = login()
        return render.search3(f)

class s:
    def GET(self):
        user_data = web.input()
        a = func(user_data.Key)
	f = login()
        return render.return1(user_data.Key,a, f)

class c:
    def GET(self):
        user_data = web.input()
        a = func2(user_data.Key)
	f = login()
        return render.return2(user_data.Key,a, f)

class i:
    def GET(self):
        user_data = web.input()
        a = func3(user_data.Key)
	f = login()
        return render.return3(user_data.Key,a, f)

if __name__ == "__main__":
    vm_env = lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    app = web.application(urls, globals())
    
    app.run()
