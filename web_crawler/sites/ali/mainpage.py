# -*- coding:utf-8-*-
import re
import sys
import time
if '../' not in sys.path:
    sys.path.append('../')

if '../../' not in sys.path:
    sys.path.append('../../')

if '../../../' not in sys.path:
    sys.path.append('../../../')
from common.commandline import CommandLine
from sites.ali.product import ComanyBySupplier
from sites.ali.product import CompanyFromProduct
from common.debug import debug
from multiprocessing import Queue, Process
from utils.dbhelper import DBHelper
from typesdefine.data_types import WebPage, Company


class AliSite(object):
    '''
    Interface for alibaba site
    '''

    def __matchAUrl(self, text):
        urlpatern = '.*(http.+htm)'
        self.pageParser = None
        return re.match(urlpatern, text).group(1)

    def __init__(self, url='http://www.1688.com', taskName='task0'):
        self.companies = []
        self.webPage = WebPage(url)
        self.webPage.pageName = 'alibaba'
        self.dbhelper = DBHelper('dbase')
        self.taskName = taskName
        initTable = 'drop table if exists `%s`' % taskName
        self.dbhelper.execute(initTable)
        company = Company()
        debug.output(company.getTitles())
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
        debug.output('searchProduct')
        url = 'http://s.1688.com/selloffer/offer_search.htm'
        postdata = {'keywords': keywords.encode('gbk')}
        product = CompanyFromProduct(url, postdata)
        q = Queue()
        p = Process(target=product.getCompanies, args=(q, ))
        p.start()
        while True:
            time.sleep(10)
            if not q.empty():
                for company in q.get():
                    if company.contactInfo:
                        company.contactInfo.displayAttributes()
                    else:
                        debug.outxput('%s,%s' % (company.companName,
                                                 company.url))
            else:
                debug.output('q is empty')

            if not p.is_alive():
                break

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
