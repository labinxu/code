# -*- coding: utf-8 -*-
import urllib.parse as parse
import urllib.request as request
from bs4 import BeautifulSoup
import sys
if '../' not in sys.path:
    sys.path.append('../')
if '../../../' not in sys.path:
    sys.path.append('../../../')
if '../../' not in sys.path:
    sys.path.append('../../')

from typesdefine.data_types import Company
from common.debug import debug
from sites.yellowpage import YellowPageParser
from sites.companypage import CompanyPageParser
from sites.certificatepage import CertifiactePageParser
from sites.contactpage import ContactInfoPageParser
from sites.pageparser import PageParser
from utils.utils import Crawler


class buildRequestData(object):
    def __init__(self, requestData):
        self.requestConf = {'keywords': 'keyboard',
                            'n': 'y',
                            'categoryId': '#',
                            'beginPage': '1',
                            'offset': '3'}


class Certifiacte(object):
    def __init__(self, company):
        self.company = company

    def getCertifiacte(self):
        pass


class CompanyFromProduct(object):
    '''
    Get the company information from product search
    '''
    def __init__(self, url, keywords):
        self.url = url
        self.keyWords = keywords
        self.companyKeyword = 'div'
        self.companyClassKeyword = 'sm-offerShopwindow-company fd-clr'
        self.companies = []
        self.splitTask = 2

    def getNumberOfPages(self, beautifulSoupObj):
        inputs = beautifulSoupObj.find_all('input',
                                           attrs={'name': 'beginPage',
                                                  'id': 'jumpto'})
        numberOfPage = None
        for input in inputs:
            numberOfPage = int(input.get('data-max'))
            break
        return numberOfPage

    def getFirstPage(self):
        postdata = parse.urlencode(self.keyWords)
        postdata = postdata.encode(encoding='utf-8')
        debug.output('open %s' % postdata)
        req = request.Request(url=self.url, data=postdata)
        result = request.urlopen(req).read()
        result = result.decode('gbk', 'ignore').encode('utf-8')
        page = BeautifulSoup(result)
        numberOfPage = self.getNumberOfPages(page)
        return (page, numberOfPage)

    def getDetails(self, company):
        try:
            pageParser = CompanyPageParser(company.url)
            certifUrl = pageParser.getCertifyInfoUrl()
            pageParser = CertifiactePageParser(certifUrl)
            yellowpageUrl = pageParser.getYellowPageUrl()
            pageParser = YellowPageParser(yellowpageUrl)
            contactUrl = pageParser.getContactInfoUrl()
            pageParser = ContactInfoPageParser(contactUrl)
            contactinfo = pageParser.getContactInfo()
            company.contactInfo = contactinfo
            if not company.contactInfo.web:
                company.contactInfo.web = company.url

        except UnicodeEncodeError as e:
            debug.error('%s' % str(e))
        except AttributeError as e:
            debug.error('AttributeError %s' % str(e))
        return company

    def getNextPage(self, page):
        if not page:
            return None

        attrs = {'class': 'page-next'}
        item = page.find('a', attrs=attrs)
        if item:
            nexpage = item.get('href')
            return PageParser(nexpage).getSoup()

    def taskGetDetails(self, companies):
        for company in companies:
            self.getDetails(company)

    def getCompanies(self):
        page, max_page = self.getFirstPage()
        self.companies = self._getCompanies(page)
        max_page = 0
        while max_page >= 0:
            max_page -= 1
            page = self.getNextPage(page)
            if page:
                self.companies.extend(self._getCompanies(page))

        return self.companies

    def _getCompanies(self, page):
        attrs = {'class': self.companyClassKeyword}
        itemattrs = {'class': 'sm-previewCompany sw-mod-previewCompanyInfo'}
        for item in page.find_all(self.companyKeyword, attrs=attrs):
            for sub in item.find_all('a', attrs=itemattrs):
                company = Company()
                company.name = sub.string.replace('\n', '')
                company.url = sub.get('href').replace('\n', '')
                company = self.getDetails(company)
                self.companies.append(company)
        return self.companies
