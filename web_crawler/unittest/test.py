# -*- coding: utf-8 -*-
import unittest

url = 'http://s.1688.com/selloffer/offer_search.htm'
postdata = {'keywords': 'keyboard'}
####################################################################
# postdata = parse.urlencode(postdata)                             #
# postdata = postdata.encode(encoding='UTF8')                      #
# req = request.Request(url=url, data=postdata)                    #
# data = request.urlopen(req).read().decode('gbk').encode('utf-8') #
#                                                                  #
# data.decode('utf-8')                                             #
####################################################################


import sys
if '../' not in sys.path:
    sys.path.append('../')

from bs4 import BeautifulSoup
from typesdefine.data_types import Company
from sites.ali.product import CompanyFromProduct


class TCompanyFromProduct(unittest.TestCase):
    def testCompanyFromProduct(self):
        companyfrom = CompanyFromProduct(url, postdata)
        res = companyfrom.getCompanies()
        for company in res:
            print(company.name)
            print(company.url)

    def testParSefile(self):

        print('testParSefile')
        f = open('test.html', 'r')
        result = f.read()
        f.close()
        page = BeautifulSoup(result)
        companies = []
        for item in page.find_all('div',
                          attrs={'class': 'sm-offerShopwindow-company fd-clr'}):

            for sub in item.find_all('a',
                                     attrs={'class': 'sm-previewCompany sw-mod-previewCompanyInfo'}):
                company = Company()
                company.name = sub.string.replace('\n', '')
                company.url = sub.get('href')
                companies.append(company)

        for company in companies:
            print(company.name, company.url)
        print(len(companies))
unittest.main()
