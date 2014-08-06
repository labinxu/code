# -*- coding: utf-8 -*-
import urllib.parse as parse
import urllib.request as request
import sys
import time
if '../' not in sys.path:
    sys.path.append('../')
if '../../../' not in sys.path:
    sys.path.append('../../../')
if '../../' not in sys.path:
    sys.path.append('../../')
from bs4 import BeautifulSoup
from typesdefine.data_types import Company
from common.debug import debug
from sites.yellowpage import YellowPageParser
from sites.companypage import CompanyPageParser
from sites.certificatepage import CertifiactePageParser
from sites.contactpage import ContactInfoPageParser
from sites.pageparser import PageParser


class CompanyBySearch(object):
    '''
    Get the company information from product search
    '''
    def __init__(self, url, keywords):
        self.url = url
        self.keyWords = keywords
        self.companies = []
        # http://s.1688.com/company/company_search.htm?keywords=keyboard

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

    def getNextPageData(self, page):
        if not page:
            return None

        attrs = {'class': 'page-next'}
        page = BeautifulSoup(page)
        item = page.find('a', attrs=attrs)
        if item:
            nexpage = item.get('href')
            counter = 3
            while counter > 0:
                try:
                    page = PageParser(nexpage).getData()
                    return page
                except Exception as e:
                    debug.error('%s will retry' % str(e))
                    counter -= 1

    def getNextPage(self, page):
        if not page:
            return None

        attrs = {'class': 'page-next'}
        item = page.find('a', attrs=attrs)
        if item:
            nexpage = item.get('href')
            counter = 3
            while counter > 0:
                try:
                    page = PageParser(nexpage).getSoup()
                    return page
                except Exception as e:
                    debug.error('%s will retry' % str(e))
                    counter -= 1

    def getCompanies(self):
        return self.companies

    def getNumberOfPages(self, beautifulSoupObj):
        inputs = beautifulSoupObj.find_all('input',
                                           attrs={'name': 'beginPage',
                                                  'id': 'jumpto'})
        numberOfPage = None
        for input in inputs:
            numberOfPage = int(input.get('data-max'))
            break
        return numberOfPage
    
    def getFirstPageData(self):
        postdata = parse.urlencode(self.keyWords)
        postdata = postdata.encode(encoding='utf-8')
        req = request.Request(url=self.url, data=postdata)
        counter = 3
        while counter > 0:
            try:
                result = request.urlopen(req).read()
                result = result.decode('gbk', 'ignore').encode('utf-8')
                page = BeautifulSoup(result)
                numberOfPage = self.getNumberOfPages(page)
                debug.output('first page max number %s' % numberOfPage)
                return (result, numberOfPage)
            except Exception as e:
                debug.error('%s will retry' % str(e))
                counter -= 1

    def getFirstPage(self):
        postdata = parse.urlencode(self.keyWords)
        postdata = postdata.encode(encoding='utf-8')
        req = request.Request(url=self.url, data=postdata)
        counter = 3
        while counter > 0:
            try:
                result = request.urlopen(req).read()
                result = result.decode('gbk', 'ignore').encode('utf-8')
                page = BeautifulSoup(result)
                numberOfPage = self.getNumberOfPages(page)
                debug.output('first page max number %s' % numberOfPage)
                return (page, numberOfPage)
            except Exception as e:
                debug.error('%s will retry' % str(e))
                counter -= 1


class ComanyBySupplier(CompanyBySearch):
    '''
    Get the company information from product search
    '''
    def __init__(self, url, keywords):
        CompanyBySearch.__init__(self, url, keywords)

    def getCompanies(self):
        page, max_page = self.getFirstPage()
        self.companies = self._getCompanies(page)
        while max_page >= 0:
            max_page -= 1
            page = self.getNextPage(page)
            if page:
                self.companies.extend(self._getCompanies(page))

        return self.companies

    def _getCompanies(self, page):
        attrs = {'class': "sw-ui-font-title14"}
        items = page.find_all('a', attrs=attrs)
        if not items:
            return []
        for item in items:
            company = Company()
            company.name = item.get('titile')
            company.url = item.get('href')
            company = self.getDetails(company)
            self.companies.append(company)
        return self.companies


class CompanyFromProduct(CompanyBySearch):
    '''
    Get the company information from product search
    '''
    def __init__(self, url, keywords):
        CompanyBySearch.__init__(self, url, keywords)
        self.companyKeyword = 'div'
        self.companyClassKeyword = 'sm-offerShopwindow-company fd-clr'
        self.companies = []
        self.splitTask = 2
        self.totalCompanies = 0

    def getCompanies(self):
        page, max_page = self.getFirstPage()
        self.companies = self._getCompanies(page)
        while max_page >= 0:
            max_page -= 1
            page = self.getNextPage(page)
            if page:
                self.companies.extend(self._getCompanies(page))

        return self.companies

    def _getCompanies(self, page):
        results = []
        attrs = {'class': self.companyClassKeyword}
        itemattrs = {'class': 'sm-previewCompany sw-mod-previewCompanyInfo'}
        companies = page.find_all(self.companyKeyword, attrs=attrs)
        for index, item in enumerate(companies):
            sub = item.find('a', attrs=itemattrs)
            company = Company()
            company.companyName = sub.string.replace('\n', '')
            company.url = sub.get('href').replace('\n', '')
            company = self.getDetails(company)
            results.append(company)
        return results
