# -*- coding:utf-8-*-
import re
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
from common.debug import debug
import multiprocessing
from utils.dbhelper import DBHelper
import socket
from typesdefine.data_types import WebPage


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
        self.dbhelper = DBHelper('../../qitong.db')
        self.taskName = taskName
        initTable = 'drop table if exists `%s`' % taskName
        self.dbhelper.execute(initTable)

        createTable = '''
        CREATE TABLE "%s" (
        "id" integer NOT NULL PRIMARY KEY,
        "company_name" varchar(100) NOT NULL,
        "company_address" varchar(200) NOT NULL,
        "company_phone_number" varchar(20) NULL,
        "company_mobilephone_number" varchar(20) NULL,
        "company_fax_number" varchar(20) NULL,
        "company_contact_person" varchar(10) NULL,
        "company_postcode" varchar(20) NULL,
        "company_web_site" varchar(100) NULL
        );''' % taskName
        self.dbhelper.execute(createTable)
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
        counter = 0
        while page:
            page = product.getNextPageData(page)
            pages.append(page)
            counter += 1
        p = multiprocessing.Pool(processes=4)
        result = []
        for page in pages:
            res = p.apply_async(GetCompanies, args=(product, page))
            result.append(res)
        p.close()
        p.join()

        for res in result:
            try:
                print(len(res.get()))
                # for company in res.get():
                #     print(company.companyName)
                #     if company.contactInfo:
                #         company.contactInfo.displayAttributes()

            except Exception as e:
                print(str(e))

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


def GetCompanies(product, page):
    companies = product._getCompanies(BeautifulSoup(page))
    return companies


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
