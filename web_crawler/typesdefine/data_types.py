# -*- coding:utf-8-*-


class Company(object):
    def __init__(self):
        self.name = ''
        self.address = ''
        self.phoneNumber = ''
        self.mobilePhone = ''
        self.detail = ''
        self.contactPerson = ''
        self.url = ''

    def setInfo(self, title, var):
        if '联系人' in title:
            self.contactPerson = var
        elif '联系电话' in title:
            self.mobilePhone = var
        elif '固定电话' in title:
            self.phoneNumber = var


class CompanyParser(object):
    def __init__(self, webData):
        self.webData = webData
        self.companies = []

    def _parse(self):
        assert self.webData is not None

    def getCompanies(self):
        return self.companies


class WebPage(object):
    def __init__(self, url):
        self.pageName = ''
        self.url = url
        self.validSearchItems = []
        self.parser = None
