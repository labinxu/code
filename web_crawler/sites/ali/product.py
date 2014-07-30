# -*- coding: utf-8 -*-
import urllib.parse as parse
import urllib.request as request
from bs4 import BeautifulSoup
import sys
if '../' not in sys.path:
    sys.path.append('../')
from typesdefine.data_types import Company


class CompanyFromProduct(object):
    def __init__(self, url, keywords):
        self.url = url
        self.keyWords = keywords
        self.companyKeyword = 'div'
        self.companyClassKeyword = 'sm-offerShopwindow-company fd-clr'

    def getCompanies(self):
        companies = []
        postdata = parse.urlencode(self.keyWords)
        postdata = postdata.encode(encoding='utf-8')
        req = request.Request(url=self.url, data=postdata)
        result = request.urlopen(req).read().decode('gbk').encode('utf-8')
        page = BeautifulSoup(result)
        attrs = {'class': self.companyClassKeyword}
        itemattrs = {'class': 'sm-previewCompany sw-mod-previewCompanyInfo'}
        for item in page.find_all(self.companyKeyword, attrs=attrs):
            for sub in item.find_all('a', attrs=itemattrs):
                company = Company()
                company.name = sub.string.replace('\n', '')
                company.url = sub.get('href')
                companies.append(company)
        return companies
