# -*- coding:utf-8-*-


class Company(object):
    def __init__(self):
        self.name = ''
        self.address = ''
        self.phoneNumber = ''
        self.detail = ''
        self.personToContact = ''
        self.url = ''

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
