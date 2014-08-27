# -*- coding:utf-8-*-
import re
import os
import sys
import concurrent.futures
if '../' not in sys.path:
    sys.path.append('../')

if '../../' not in sys.path:
    sys.path.append('../../')

if '../../../' not in sys.path:
    sys.path.append('../../../')
from sites.ali.product import ComanyBySupplier
from sites.ali.product import CompanyFromProduct
from utils import debug
import socket
from typesdefine.data_types import WebPage
from bs4 import BeautifulSoup
from typesdefine import Enterprise
from db import DBHelper


def GetParser():
    return AliSite()


class AliSite(object):
    '''
    Interface for alibaba site
    '''

    def __matchAUrl(self, text):
        urlpatern = '.*(http.+htm)'
        self.pageParser = None
        return re.match(urlpatern, text).group(1)

    def __init__(self, url='http://www.1688.com', taskName='task0'):
        timeout = 10
        socket.setdefaulttimeout(timeout)

        self.companies = []
        self.webPage = WebPage(url)
        self.webPage.pageName = 'alibaba'
        self.taskName = None
        # company = Company()
        # company.getTitles())
        # ['phoneNumber', 'faxNumber', 'web', 'address', 'contactPerson',
        # 'mobilePhone', 'postcode', 'majorBusiness', 'majorProduct']

        # self.pageParser = PageParser(url)
        # soup = self.pageParser.getSoup()
        # for list in soup.find_all('form'):
        #     for itemli in list.find_all('li'):
        #         dataConf = itemli.get('data-config')
        #         item = itemli.find('a')
        #         temp = (item.string, self.__matchAUrl(dataConf))
        #         self.webPage.validSearchItems.append(temp)
        # # # input keywords
        # input = soup.find('input', attrs={'id': 'keywordinput'})
        # self.webPage.postKeywords = input.get('name')

    def searchProduct(self, keywords):
        url = 'http://s.1688.com/selloffer/offer_search.htm'
        postdata = {'keywords': keywords.encode('gbk')}
        product = CompanyFromProduct(url, postdata)
        page, _ = product.getFirstPageData()
        pages = []
        pages.append(page)
        counter = 3
        while page and counter > 0:
            page = product.getNextPageData(page)
            pages.append(page)
            counter -= 1
            
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = {executor.submit(GetCompanies,
                                       product,
                                       page): page for page in pages}
            maxnumer = len(futures)
            finished = 0
            for future in concurrent.futures.as_completed(futures):
                try:
                    ents = future.result()
                except Exception as exc:
                    debug.error(str(exc))
                else:
                    finished += 1
                    self.runStatus[self.taskName] = (finished / maxnumer) * 100
                    debug.info('progress %s' % self.runStatus[self.taskName])
                    for ent in ents:
                        ent.save()

    def searchSupplier(self, keywords):
        url = 'http://s.1688.com/company/company_search.htm'
        postdata = {'keywords': keywords.encode('gbk')}

        supplier = ComanyBySupplier(url, postdata)
        self.companies = supplier.getCompanies()

        for company in self.companies:
            if company.contactInfo:
                company.contactInfo.displayAttributes()
            else:
                debug.output('%s, %s' % (company.companName, company.url))

    def startTask(self, taskName, progress, product=None, supplier=None):
        dbname = '%s.db' % taskName
        if os.path.exists(dbname):
            DBHelper.getInstance(dbname)
        else:
            dbhelper = DBHelper.getInstance(dbname)
            dbhelper.execute(Enterprise.__init_table__)
        self.taskName = taskName
        self.runStatus = progress
        if product:
            self.searchProduct(product)
        else:
            self.searchSupplier(supplier)


def GetCompanies(product, page):
    companies = product._getCompanies(BeautifulSoup(page))
    return companies


# def main():
#     params, _ = CommandLine().parseCmdLine()
#     aliSite = AliSite()
#     if params.SUPPLIER:
#         debug.output('Searching %s' % params.SUPPLIER)
#         aliSite.searchSupplier(params.SUPPLIER)
#     elif params.PRODUCT:
#         debug.output('Searching %s' % params.PRODUCT)
#         aliSite.searchProduct(params.PRODUCT)

#     # province=
# if __name__ == '__main__':
#     main()
