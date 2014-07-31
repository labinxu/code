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


class buildRequestData(object):
    def __init__(self, requestData):
        self.requestConf = {'keywords': 'keyboard',
                            'n': 'y',
                            'categoryId': '#',
                            'beginPage': '1',
                            'offset': '3'}


class CompanyFromProduct(object):
    '''
    Get the company information from product search
    '''
    def __init__(self, url, keywords):
        self.url = url
        self.keyWords = keywords
        self.companyKeyword = 'div'
        self.companyClassKeyword = 'sm-offerShopwindow-company fd-clr'
        self.companies = {}

    def __getBeautifulObj(self, url):
        if not url:
            return None
        debug.output('Parsing %s' % url)
        response = request.urlopen(url)
        html = response.read()
        data = html.decode('gbk', 'ignore').replace('&nbsp', '')
        data = data.encode('utf-8')
        return BeautifulSoup(data)
        
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
        req = request.Request(url=self.url, data=postdata)
        debug.output('Parsing %s' % req)
        result = request.urlopen(req).read()
        result = result.decode('gbk', 'ignore').encode('utf-8')
        page = BeautifulSoup(result)
        numberOfPage = self.getNumberOfPages(page)
        debug.output('max page is %d' % numberOfPage)
        return (page, numberOfPage)

    def getDetails(self, company):
        assert(company is not None)
        try:
            detailPage = self.__getBeautifulObj(company.url)
            moreDetail = detailPage.find('a',
                                         attrs={'class': 'certificate-etp '})
            if not moreDetail:
                moreDetail = detailPage.find('a',
                                             attrs={'class': 'certificate '})
       
            moreDetailUrl = moreDetail.get('href')
            moreDetail = self.__getBeautifulObj(moreDetailUrl)
            # get contactperson
            attrs = {'id': 'memberinfo'}
            detail = moreDetail.find('div', attrs=attrs)
            detailFrame = detail.find('dl')
            contens = detailFrame.find_all('dd')
            for content in contens:
                title, var = content.text.replace(';', '').split('：')
                company.setInfo(title, var)
        except UnicodeEncodeError as e:
            debug.error(str(e))
        except AttributeError as e:
            debug.error(str(e))
        return company

    def getNextPage(self, page):
        if not page:
            return None

        attrs = {'class': 'page-next'}
        item = page.find('a', attrs=attrs)
        if item:
            nexpage = item.get('href')
            return self.__getbeautifulObj(nexpage)

    def getCompanies(self):
        page, max_page = self.getFirstPage()
        self.companies = self._getCompanies(page)
        max_page = 1
        while max_page >= 0:
            max_page -= 1
            page = self.getNextPage(page)
            if page:
                self.companies.update(self._getCompanies(page))
        return self.companies

    def _getCompanies(self, page):
        attrs = {'class': self.companyClassKeyword}
        itemattrs = {'class': 'sm-previewCompany sw-mod-previewCompanyInfo'}
        for item in page.find_all(self.companyKeyword, attrs=attrs):
            for sub in item.find_all('a', attrs=itemattrs):
                company = Company()
                company.name = sub.string.replace('\n', '')
                company.url = sub.get('href')
                company = self.getDetails(company)
                self.companies[company.name] = company
        return self.companies
