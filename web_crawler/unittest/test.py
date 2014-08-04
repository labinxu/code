# -*- coding: utf-8 -*-
import unittest
import sys
if '../' not in sys.path:
    sys.path.append('../')
from typesdefine.data_types import Company
from sites.companypage import CompanyPageParser
from sites.certificatepage import CertifiactePageParser
from sites.yellowpage import YellowPageParser


class TCompanyFromProduct(unittest.TestCase):
    def setUp(self):
        self.company = Company()

    # def testCompanyFromProduct(self):
    #     from sites.ali.product import CompanyFromProduct
    #     url = 'http://s.1688.com/selloffer/offer_search.htm'
    #     s = '键盘'
    #     postdata = {'keywords': s.encode('gbk')}
    #     companyfrom = CompanyFromProduct(url, postdata)
    #     res = companyfrom.getCompanies()
    #     for company in res:
    #         print('=============================')
    #         company.contactInfo.displayAttributes()

    def testCompanyFromSupplier(self):
        print('testCompanyFromSupplier')
        from sites.ali.product import ComanyBySupplier
        url = 'http://s.1688.com/company/company_search.htm'
        s = '袜子'
        postdata = {'keywords': s.encode('gbk')}
        companyfrom = ComanyBySupplier(url, postdata)
        res = companyfrom.getCompanies()
        for company in res:
            print('=============================')
            company.contactInfo.displayAttributes()

    # def testCompanyPageParser(self):
    #     from sites.companypage import CompanyPageParser
    #     from sites.certificatepage import CertifiactePageParser
    #     from sites.yellowpage import YellowPageParser

    #     pageParser = CompanyPageParser('http://shop1355395132054.1688.com')
    #     dest = 'http://shop1355395132054.1688.com/page/creditdetail.htm#certifyInfo'
    #     self.assertEqual(dest, pageParser.getCertifyInfoUrl())
    #     pageParser = CertifiactePageParser(pageParser.getCertifyInfoUrl())
    #     dest = 'http://exodus.1688.com/company/detail/jeqang8.html?fromSite=company_site&tracelog=gsda_huangye'
    #     self.assertEqual(dest, pageParser.getYellowPageUrl())
    #     pageParser = YellowPageParser(pageParser.getYellowPageUrl())
        # print(pageParser.getBaseInfoUrl())
        # print(pageParser.getContactInfoUrl())
        # print(pageParser.getOperateStatusUrl())
        
    # def testContactPage(self):
    #     print('test Contact page')
    #     url = 'http://www.1688.com/company/jeqang8.html?fromSite=company_site&tab=companyWeb_contact'
    #     from sites.contactpage import ContactInfoPageParser

    #     pageParser = ContactInfoPageParser(url)
    #     # pageParser.getContactInfo().displayAttributes()

    # def testMoreDetail(self):
    #     self.company.url = 'http://shop1355395132054.1688.com'
    #     from sites.ali.product import CompanyFromProduct
    #     companyfrom = CompanyFromProduct(None, None)
    #     companyfrom.getDetails(self.company).contactInfo.displayAttributes()

    # def testClawerThread(self):
    #     url = 'http://www.1688.com/company/jeqang8.html?fromSite=company_site&tab=companyWeb_contact'
    #     from sites.contactpage import ContactInfoPageParser
    #     pageParser = ContactInfoPageParser(url)
    #     from utils.utils import Crawler
    #     crawler = Crawler(pageParser.getContactInfo)
    #     crawler.start()
    #     crawler.join(10)
    #     print('main thread')
    #     crawler.result.displayAttributes()

    # def testParSefile(self):
    #     f = open('test.html', 'r')
    #     result = f.read()
    #     f.close()
    #     page = BeautifulSoup(result)
    #     companies = []
    #     attrs = {'class': 'sm-offerShopwindow-company fd-clr'}
    #     subattrs = {'class': 'sm-previewCompany sw-mod-previewCompanyInfo'}
    #     for item in page.find_all('div', attrs=attrs):
    #         for sub in item.find_all('a', attrs=subattrs):
    #             company = Company()
    #             company.name = sub.string.replace('\n', '')
    #             company.url = sub.get('href')
    #             companies.append(company)

    #     for company in companies:
    #         # print(company.name, company.url)
    #         pass
    #     print(len(companies))

    def testAlisite(self):
        from sites.ali.mainpage import AliSite
        ali = AliSite()
        for pageitem in ali.webPage.validSearchItems:
            print(pageitem)
        print(ali.webPage.postKeywords)
unittest.main()
