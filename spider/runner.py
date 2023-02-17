# coding=utf-8
# !/usr/bin/python
import os
from importlib.machinery import SourceFileLoader
from urllib import parse

import requests


def createFile(file_path):
    if os.path.exists(file_path) is False:
        os.makedirs(file_path)


def redirectResponse(tUrl):
    rsp = requests.get(tUrl, allow_redirects=False, verify=False)
    if 'Location' in rsp.headers:
        return redirectResponse(rsp.headers['Location'])
    else:
        return rsp


def downloadFile(name, url):
    try:
        rsp = redirectResponse(url)
        with open(name, 'wb') as f:
            f.write(rsp.content)
        print(url)
    except:
        print(name + ' =======================================> error')
        print(url)


def downloadPlugin(basePath, url):
    createFile(basePath)
    name = url.split('/')[-1].split('.')[0]
    pyName = ''
    if url.startswith('file://'):
        pyName = url.replace('file://', '')
    else:
        pyName = basePath + name + '.py'
        downloadFile(pyName, url)
    paramList = parse.parse_qs(parse.urlparse(url).query).get('extend')
    if paramList == None:
        paramList = ['']
    return pyName


def loadFromDisk(fileName):
    name = fileName.split('/')[-1].split('.')[0]
    sp = SourceFileLoader(name, fileName).load_module().Spider()
    return sp


class Runner():  # 元类 默认的元类 type
    def __init__(self, spiderName):
        self.spider = loadFromDisk(spiderName)

    def getDependence(self):
        return self.spider.getDependence()

    def getName(self):
        return self.spider.getName()

    def init(self, extend=""):
        self.spider.init(extend)

    def homeContent(self, filter):
        return self.spider.homeContent(filter)

    def homeVideoContent(self):
        return self.spider.homeVideoContent()

    def categoryContent(self, tid, pg, filter, extend):
        return self.spider.categoryContent(tid, pg, filter, extend)

    def detailContent(self, ids):
        return self.spider.detailContent(ids)

    def searchContent(self, key, quick):
        return self.spider.searchContent(key, quick)

    def playerContent(self, flag, id, vipFlags):
        return self.spider.playerContent(flag, id, vipFlags)

    def localProxy(self, param):
        return self.spider.localProxy(param)

    def isVideoFormat(self, url):
        return self.spider.isVideoFormat(url)

    def manualVideoCheck(self):
        return self.spider.manualVideoCheck()
