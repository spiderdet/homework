import sys, os

#建立图片索引所需的txt文件

if __name__ == '__main__':

    reload(sys)
    sys.setdefaultencoding('utf-8')

    count = 0
    root = 'html'
    file1 = open('img.txt', 'w')
    for root, dirnames, filenames in os.walk(root):
        for filename in filenames:
            print "adding", filename
            count += 1
            try:
                path = os.path.join(root, filename)
                file = open(path)
                content = unicode(file.read(), 'utf-8')
                content = content.encode('utf-8')
                list1 = content.split('\n')
                file.close()

                img_url = list1[3]
                print('img_url : ' + img_url)
                name = list1[1]
                print('name : ' + name)
                file1.write(name + '\t' + img_url + '\n')

            except Exception, e:
                print "Failed in picindexing:", e
    file1.close()
    print(count)