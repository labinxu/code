# -*- coding: utf-8 -*-
import sys
import urllib.request as request
from bs4 import BeautifulSoup
if '../../' not in sys.path:
    sys.path.append('../../')
from common.debug import debug


class PageParser(object):
    def __init__(self, pageurl):
        self.pageUrl = pageurl
        self.soup = None

    def _findItemByAttrs(self, attrs):
        soup = self.getSoup()
        item = soup.find('input', attrs=attrs)
        return item

    def getSoup(self):
        if self.soup:
            return self.soup
        response = request.urlopen(self.pageUrl)
        debug.output('parsing %s' % self.pageUrl)
        html = response.read()
        data = html.decode('gbk', 'ignore').replace('&nbsp', '')
        data = data.encode('utf-8')
        self.soup = BeautifulSoup(data)
        return self.soup
