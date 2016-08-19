#!/usr/bin/env python
#  -*- coding: UTF-8 -*-
import os
import os.path

import sys
import time
import exifread
reload(sys)
sys.setdefaultencoding('utf8')

PHOTO_TYPE = ['.jpg', '.png', '.bmp', '.jpeg']
VIDEO_TPYE = ['.mpg', '.mp4', '.avi', '.mov']

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

        # rename
        # 需要替换的字符
        self.__start = "IMG_"
        # 需要替换成的字符
        self.__end = ""

        # retype
        # 后缀名
        self.__type = ".txt"
        # 是否修改后缀名
        self.__typechange = True

        # attrname
        # 根据属性对文件进行重命名
        self.__checktype = False
        self.__attrtype = ".jpg"

    # 根据字符判断对文件进行重命名
    def fileexist(self, path, filename):
        try:
            size = os.path.getsize(os.path.join(path, filename))
            name = os.path.splitext(filename)[0]
            sufix = os.path.splitext(filename)[1]
            for i in range(1000):
                newname = name + bytes(i) + sufix
                try:
                    size = os.path.getsize(os.path.join(path, newname)) == 0
                except:
                    return newname
        except:
            return filename

    # 根据字符判断对文件进行重命名
    def rename(self,path,srcname,detname):
        if cmp(srcname,detname) == 0:
            return
        os.chdir(path)
        newname = self.fileexist(path,detname)
        if (os.path.isdir(os.path.join(path, srcname)) and self.__dir):
            self.__path.append(os.path.join(path, newname).decode('gb2312'))
        if not(os.path.isdir(os.path.join(path,srcname)) and not(self.__dir)):
            try:
                os.rename(os.path.join(path,srcname),os.path.join(path, newname))
                print "rename:" + os.path.join(path,srcname).decode('gb2312') + "-->" + newname.decode('gb2312')
            except:
                print "---fail:" + os.path.join(path, srcname).decode('gb2312') + "-->" + newname.decode('gb2312')
        return

    # 根据字符判断对文件进行重命名
    def replace(self):
        if self.__filename.find(self.__src.encode('cp936')) >= 0:
            # 替换字符串的字符
            name = self.__filename.replace(self.__src.encode('cp936'),self.__des.encode('cp936'))
            self.rename(self.__parent,self.__filename,name)
        return

    # 为文件名加上前后缀
    def add(self):
        if self.__filename[:len(self.__start)].find(self.__start.encode('cp936')) >= 0:
            self.__start = ""
        if self.__filename[-len(self.__end):].find(self.__end.encode('cp936')) >= 0:
            self.__end = ""
        if self.__start == "" and self.__end == "":
            return

        name = self.__start + self.__filename + self.__end
        if os.path.splitext(self.__filename)[0]:
            name = self.__start + os.path.splitext(self.__filename)[0] + self.__end + os.path.splitext(self.__filename)[1]
        self.rename(self.__parent,self.__filename,name)
        return

    # 添加或者修改文件的后缀
    def retype(self):
        name = self.__filename
        if os.path.isdir(os.path.join(self.__parent,self.__filename)):
            return
        sufix = os.path.splitext(self.__filename)[1]
        if self.__typechange and sufix:
            name = self.__filename.replace(sufix, self.__type)
        elif not sufix:
            name = self.__filename + self.__type
        else:
            return
        self.rename(self.__parent, self.__filename, name)
        return

    # 根据属性对文件进行重命名
    def attrname(self):
        sufix = os.path.splitext(self.__filename)[1]
        if sufix != self.__attrtype and self.__checktype:
            return
        name = self.getfileattr("size", self.__filename)
        if name == None:
            return
        name = self.__start + name + sufix

        self.rename(self.__parent, self.__filename, name)
        return

    # 修改照片文件名 IMG_20160706_122627.jpg
    def rephoto(self):
        sufix = os.path.splitext(self.__filename)[1]
        if sufix.lower() not in PHOTO_TYPE:
            return
        if self.__filename[:4].find("IMG_") >= 0 and len(self.__filename) > 22:
            return
        name = self.getfileattr("photo", self.__filename)
        if name == None:
            return
        name = "IMG_" + name + "." + sufix.lower()
        self.rename(self.__parent, self.__filename, name)
        return

    # 删除空目录
    def rmnulldir(self):
        dir = os.path.join(self.__parent, self.__filename)
        if not os.path.isdir(dir):
            return
        try:
            if not os.listdir(dir):
                os.rmdir(dir)
                print 'del null dir:', dir.decode('gb2312')
        except:
            print  "del fail[%s]\n" % dir.decode('gb2312')
        return

    # 删除空文件
    def rmnullfile(self):
        file = os.path.join(self.__parent, self.__filename)
        if os.path.isdir(file):
            return
        try:
            if 0 == os.stat(file).st_size:
                os.remove(file)
                print 'del null file:', file.decode('gb2312')
        except:
            print  "del fail[%s]\n" % file.decode('gb2312')
        return

    def getfileattr(self,type,name):
        if type == "photo":
            # 获取照片拍摄时间
            try:
                file = open(os.path.join(self.__parent,name), 'rb')
                data = exifread.process_file(file)
                if data:
                    try:
                        time = data['EXIF DateTimeOriginal']
                        time = str(time).replace(":", "")
                        #print time
                        return str(time).replace(" ", "_")
                    except:
                        pass
            except:
                print  "open fail[%s]\n" % name
        elif type == "access":
            # 最后访问时间
            statinfo = os.stat(os.path.join(self.__parent, self.__filename))
            filetime = statinfo.st_atime
        elif type == "modify":
            # 最后修改时间
            statinfo = os.stat(os.path.join(self.__parent, self.__filename))
            filetime = statinfo.st_mtime
        elif type == "creat":
            # 创建时间
            statinfo = os.stat(os.path.join(self.__parent, self.__filename))
            filetime = statinfo.st_ctime
        elif type == "size":
            # 文件大小
            statinfo = os.stat(os.path.join(self.__parent, self.__filename))
            return bytes(statinfo.st_size)
        # %Y-%m-%d %H:%M:%S
        # %Y%m%d_%H%M%S
        return time.strftime("%Y%m%d_%H%M%S", time.localtime(filetime))
        return

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
                fun()

            for filename in filenames:  # 输出文件信息
                self.__parent = parent
                self.__filename = filename
                #print "the full name of the file is:" + os.path.join(parent, filename).decode('gb2312')  # 输出文件路径信息
                fun()
        return
    def functions(self,type):
        switcher = {
            0: self.replace,
            1: self.add,
            2: self.attrname,
            3: self.rephoto,
            4: self.retype,
            5: self.rmnulldir,
            6: self.rmnullfile
        }
        return switcher.get(type,self.rmnulldir)

    def setpara(self,type):
        if type == 0:
            self.__src = raw_input("Input the str want to replace:")
            self.__des = raw_input("Input the str replace to:")
        elif type == 1:
            self.__start = raw_input("Input the str add before:")
            self.__end = raw_input("Input the str add behind:")
        elif type == 2:
            pass
        return

def main():
    print "************************"
    print "*  0. replace name     *"
    print "*  1. filename add     *"
    print "*  2. rename with attr *"
    print "*  3. rename photo     *"
    print "*  4. retype file      *"
    print "*  5. del null dir     *"
    print "*  6. del null file    *"
    print "************************"
    type = input("input option: ")

    ftls = FileEdit()
    # ftls.setpara()
    while ftls.count():
        ftls.loop(ftls.functions(type))
    print "Job Done."

if __name__ == '__main__':
    main()