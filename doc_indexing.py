#!/usr/bin/env python

INDEX_DIR = "IndexFiles.index"

#建立文本索引

import sys, os, lucene, threading, time, urllib2
import urlparse
from datetime import datetime
from bs4 import BeautifulSoup
from java.io import File
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.core import WhitespaceAnalyzer
from org.apache.lucene.document import Document, Field, FieldType
from org.apache.lucene.index import FieldInfo, IndexWriter, IndexWriterConfig
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.util import Version

"""
This class is loosely based on the Lucene (java implementation) demo class
org.apache.lucene.demo.IndexFiles.  It will take a directory as an argument
and will index all of the files in that directory and downward recursively.
It will index on the file path, the file name and the file contents.  The
resulting Lucene index will be placed in the current directory and called
'index'.
"""


class Ticker(object):
    def __init__(self):
        self.tick = True

    def run(self):
        while self.tick:
            sys.stdout.write('.')
            sys.stdout.flush()
            time.sleep(1.0)


class IndexFiles(object):
    """Usage: python IndexFiles <doc_directory>"""

    def __init__(self, root, indextxt, storeDir, analyzer):

        if not os.path.exists(storeDir):
            os.mkdir(storeDir)

        store = SimpleFSDirectory(File(storeDir))
        analyzer = LimitTokenCountAnalyzer(analyzer, 1048576)
        config = IndexWriterConfig(Version.LUCENE_CURRENT, analyzer)
        config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
        writer = IndexWriter(store, config)

        self.indexDocs(root, indextxt, writer)
        ticker = Ticker()
        print 'commit index'
        threading.Thread(target=ticker.run).start()
        writer.commit()
        writer.close()
        ticker.tick = False
        print 'done'

    def indexDocs(self, root, indextxt, writer):

        t1 = FieldType()
        t1.setIndexed(True)   #t1为需索引, 需保存, 需分词
        t1.setStored(True)
        t1.setTokenized(True)
        t1.setIndexOptions(FieldInfo.IndexOptions.DOCS_AND_FREQS)

        t2 = FieldType()     #t2为不需索引, 需保存, 需分词
        t2.setIndexed(False)
        t2.setStored(True)
        t2.setTokenized(True)
        t2.setIndexOptions(FieldInfo.IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)

        for root, dirnames, filenames in os.walk(root):
            for filename in filenames:

                print "adding", filename
                try:
                    path = os.path.join(root, filename)
                    file = open(path)
                    content = unicode(file.read(), 'utf-8')
                    content = content.encode('utf-8')
                    list1 = content.split('\n')
                    file.close()

                    doc = Document()

                   # 读取存于文件的内容并保存于doc
                    url = list1[0]
                    print('url : ' + url)
                    doc.add(Field("url", url, t1))

                    name = list1[1]
                    print('name : ' + name)
                    doc.add(Field("name", name, t1))

                    collectnum = list1[2]
                    print('collect_num : ' + collectnum)
                    doc.add(Field("collect_num", collectnum, t2))

                    img_url = list1[3]
                    print('img_url : ' + img_url)
                    doc.add(Field("img_url", img_url, t2))

                    zhuliao = list1[4]
                    print(zhuliao)
                    doc.add(Field("zhuliao", zhuliao, t1))

                    zuofa = list1[5]
                    zuofa = '\n'.join(zuofa.split('\t'))
                    print('zuofa : ' + zuofa)
                    doc.add(Field("zuofa", zuofa, t2))

                    writer.addDocument(doc)
                except Exception, e:
                    print "Failed in indexDocs:", e


if __name__ == '__main__':
    """
    if len(sys.argv) < 2:
        print IndexFiles.__doc__
        sys.exit(1)
    """
    reload(sys)
    sys.setdefaultencoding('utf-8')

    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    print 'lucene', lucene.VERSION
    start = datetime.now()
    try:
        """
        base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        IndexFiles(sys.argv[1], os.path.join(base_dir, INDEX_DIR),
                   StandardAnalyzer(Version.LUCENE_CURRENT))
                   """
        analyzer = WhitespaceAnalyzer(Version.LUCENE_CURRENT)
        IndexFiles('html', 'index.txt', "index", analyzer)
        end = datetime.now()
        print end - start
    except Exception, e:
        print "Failed: ", e
