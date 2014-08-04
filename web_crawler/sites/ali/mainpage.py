# -*- coding:utf-8-*-
from bs4 import BeautifulSoup
import re
import urllib.request as request
import sys
if '../' not in sys.path:
    sys.path.append('../')

if '../../' not in sys.path:
    sys.path.append('../../')

if '../../../' not in sys.path:
    sys.path.append('../../../')
from common.commandline import CommandLine
from sites.ali.product import ComanyBySupplier
from sites.ali.product import CompanyFromProduct
from sites.pageparser import PageParser
from common.debug import debug


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
        self.pageParser = None
        return re.match(urlpatern, text).group(1)

    def __init__(self, url='http://www.1688.com'):
        self.pageParser = PageParser(url)

        soup = self.pageParser.getSoup()
        self.webPage = WebPage(url)
        self.webPage.pageName = 'alibaba'
        soup = self.pageParser.getSoup()
        for list in soup.find_all('form'):
            pass
        #     for itemli in list.find_all('li'):
        #         dataConf = itemli.get('data-config')
        #         item = itemli.find('a')
        #         temp = (item.string, self.__matchAUrl(dataConf))
        #         self.webPage.validSearchItems.append(temp)

        # # input keywords
        # input = soup.find('input', attrs={'id': 'keywordinput'})
        # self.webPage.postKeywords = input.get('name')

    def searchProduct(self, keywords):
        url = 'http://s.1688.com/selloffer/offer_search.htm'
        postdata = {'keywords': keywords.encode('gbk')}
        product = CompanyFromProduct(url, postdata)
        res = product.getCompanies()
        for company in res:
            company.contactInfo.displayAttributes()

    def searchSupplier(self, keywords):
        url = 'http://s.1688.com/company/company_search.htm'
        postdata = {'keywords': keywords.encode('gbk')}

        supplier = ComanyBySupplier(url, postdata)
        res = supplier.getCompanies()
        for company in res:
            company.contactInfo.displayAttributes()


def main():
    params, _ = CommandLine().parseCmdLine()
    aliSite = AliSite()
    if params.SUPPLIER:
        debug.output('Searching %s' % params.SUPPLIER)
        aliSite.searchSupplier(params.SUPPLIER)
    elif params.PRODUCT:
        debug.output('Searching %s' % params.PRODUCT)
        aliSite.searchProduct(params.PRODUCT)

    # province=
        
if __name__ == '__main__':
    main()
