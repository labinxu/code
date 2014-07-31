# -*- coding: utf-8 -*-
import unittest


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
    def setUp(self):
        pass

    def testCompanyFromProduct(self):
        url = 'http://s.1688.com/selloffer/offer_search.htm'
        s = '键盘'
        postdata = {'keywords': s.encode('gbk')}
        print(postdata)
        companyfrom = CompanyFromProduct(url, postdata)
        res = companyfrom.getCompanies()
        print(len(res))
        f = open('contacts.txt', 'w')
        for company in res.values():
            f.write(company.name)
            f.write(company.url)
            f.write(company.contactPerson)
            f.write(company.mobilePhone)
            f.write(company.phoneNumber)
        f.close()

    def testMoreDetail(self):
        company = Company()
        company.url = 'http://shop1355395132054.1688.com'
        companyfrom = CompanyFromProduct(None, None)
        companyfrom.getDetails(company)

    def testParSefile(self):
        f = open('test.html', 'r')
        result = f.read()
        f.close()
        page = BeautifulSoup(result)
        companies = []
        attrs = {'class': 'sm-offerShopwindow-company fd-clr'}
        subattrs = {'class': 'sm-previewCompany sw-mod-previewCompanyInfo'}
        for item in page.find_all('div', attrs=attrs):
            for sub in item.find_all('a', attrs=subattrs):
                company = Company()
                company.name = sub.string.replace('\n', '')
                company.url = sub.get('href')
                companies.append(company)

        for company in companies:
            print(company.name, company.url)
        print(len(companies))
    def testAlisite(self):
        from sites.ali.mainpage import AliSite
        ali = AliSite()
        for pageitem in ali.webPage.validSearchItems:
            print(pageitem)
        print(ali.webPage.postKeywords)
unittest.main()
