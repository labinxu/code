# -*- coding:utf-8-*-
from bs4 import BeautifulSoup
import re
import urllib.request as request
import sys
if '../../' not in sys.path:
    sys.path.append('../../')


class WebPage(object):
    def __init__(self, url):
        self.pageName = ''
        self.url = url
        self.validSearchItems = []
        self.parser = None
        self.postKeywords = ''


class AliSite(object):

    def __matchAUrl(self, text):
        urlpatern = '.*(http.+htm)'
        return re.match(urlpatern, text).group(1)

    def __init__(self, url='http://www.1688.com'):
        response = request.urlopen(url)
        html = response.read()
        data = html.decode('gbk').encode('utf-8')
        soup = BeautifulSoup(data)
        self.webPage = WebPage(url)
        self.webPage.pageName = 'alibaba'

        for list in soup.find_all('form'):
            for itemli in list.find_all('li'):
                dataConf = itemli.get('data-config')
                item = itemli.find('a')
                temp = (item.string, self.__matchAUrl(dataConf))
                self.webPage.validSearchItems.append(temp)

        # input keywords
        input = soup.find('input', attrs={'id': 'keywordinput'})
        self.webPage.postKeywords = input.get('name')
