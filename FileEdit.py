#!/usr/bin/env python
#  -*- coding: UTF-8 -*-
import os
import os.path

import sys
reload(sys)
sys.setdefaultencoding('utf8')


class FileEdit:
    def __init__(self):
        self.__parent = ''
        self.__filename = ''

        # 需要操作的目录
        self.__path = ["D:\\测试123"]

        # 是否删除空目录
        self.__null = True

        # rename
        # 需要替换的字符
        self.__src = "ccc"
        # 需要替换成的字符
        self.__des = "ddd"
        # 是否替换目录
        self.__dir = True

        # retype
        # 后缀名
        self.__type = ".txt"
        # 是否修改后缀名
        self.__typechange = False

    # 根据字符判断对文件进行重命名
    def rename(self):
        if self.__filename.find(self.__src.encode('cp936')) >= 0:
            # 替换字符串的字符
            name = self.__filename.replace(self.__src.encode('cp936'),self.__des.encode('cp936'))
            os.chdir(self.__parent)
            if (os.path.isdir(os.path.join(self.__parent, self.__filename)) and self.__dir):
                self.__path.append(os.path.join(self.__parent,name).decode('gb2312'))
            if not(os.path.isdir(os.path.join(self.__parent,self.__filename)) and not(self.__dir)):
                os.rename(os.path.join(self.__parent,self.__filename),os.path.join(self.__parent,name))
                print "rename:" + os.path.join(self.__parent,self.__filename).decode('gb2312') + "-->" + name.decode('gb2312')
        return

    # 添加或者修改文件的后缀
    def retype(self):
        name = self.__filename
        if os.path.isdir(os.path.join(self.__parent,self.__filename)):
            return
        sufix = os.path.splitext(self.__filename)[1][1:]
        if self.__typechange and sufix:
            sufix = "." + sufix
            name = self.__filename.replace(sufix, self.__type)
        elif not sufix:
            # 替换字符串的字符
            name = self.__filename + self.__type
        else:
            return
        os.chdir(self.__parent)
        os.rename(os.path.join(self.__parent,self.__filename),os.path.join(self.__parent,name))
        print "rename:" + os.path.join(self.__parent,self.__filename).decode('gb2312') + "-->" + name.decode('gb2312')
        return

    # 删除空目录
    def rmnulldir(self,curdir):
        if not os.listdir(curdir):
            os.rmdir(curdir)
            print 'del null dir:', curdir.decode('gb2312')
            return True
        return False

    # 队列目录数
    def count(self):
        return len(self.__path)

    # 循环遍历
    def loop(self, fun):
        # 三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
        scanpath = self.__path.pop()
        for parent, dirnames, filenames in os.walk(scanpath.encode('cp936')):
            # 输出文件夹信息
            for dirname in dirnames:
                self.__parent = parent
                self.__filename = dirname
                #print "parent:" + parent.decode('gb2312') + "-->filename:" + dirname.decode('gb2312')
                isdell = False
                if self.__null:
                    isdell = self.rmnulldir(os.path.join(parent, dirname))
                if not isdell:
                    fun()

            for filename in filenames:  # 输出文件信息
                self.__parent = parent
                self.__filename = filename
                #print "the full name of the file is:" + os.path.join(parent, filename).decode('gb2312')  # 输出文件路径信息
                fun()
        return

def main():
    ftls = FileEdit()
    while ftls.count():
        ftls.loop(ftls.rename)
    print "Job Done."

if __name__ == '__main__':
    main()

