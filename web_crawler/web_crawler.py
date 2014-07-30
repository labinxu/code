# -*- coding:utf-8-*-


class Company(object):
    def __init__(self):
        self.name = ''
        self.address = ''
        self.phoneNumber = ''
        self.detail = ''
        self.personToContact = ''


class CompanyParser(object):
    def __init__(self, webData):
        self.webData = webData
        self.companies = []

    def _parse(self):
        assert self.webData is not None

    def getCompanies(self):
        return self.companies


class WebPage(object):
    def __init__(self, url):
        self.pageName = ''
        self.url = url
        self.validSearchItems = []
        self.parser = None


import urllib.request as request

from bs4 import BeautifulSoup
import re


def matchAUrl(text):
    urlpatern = '.*(http.+htm)'
    return re.match(urlpatern, text).group(1)
    

def taobao_main(url):
    response = request.urlopen(url)
    html = response.read()
    data = html.decode('gbk').encode('utf-8')
    soup = BeautifulSoup(data)
    webPage = WebPage(url)
    webPage.pageName = 'taobao'
    for list in soup.find_all('form'):
        for itemli in list.find_all('li'):
            dataConf = itemli.get('data-config')
            item = itemli.find('a')
            webPage.validSearchItems.append((item.string, matchAUrl(dataConf)))
        break

    print(str(webPage.validSearchItems))

if __name__ == '__main__':
    import sys
    if '../' not in sys.path:
        sys.path.append('../')
    from common.commandline import CommandLine

    # url = 'http://www.taobao.com/?spm=a310q.2219005.1581860521.1.b9kUd4'
    cmdline = CommandLine()
    args, _ = cmdline.parseCmdLine()
    print(args.product)

    url = 'http://www.1688.com'
    # taobao_main(url)
    # .*(http.+htm)
