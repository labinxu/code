# -*- coding:utf-8-*-


class PageData(object):
    def displayAttributes(self):
        for name, value in vars(self).items():
            print('%s = %s' % (name, value))

    def storeSting(self):
        titles = []
        values = []
        for name, value in vars(self).items():
            titles.append(name)
            values.append(value)
        return (titles, values)

    def getTitles(self):
        titles = []
        for name, value in vars(self).items():
            titles.append(name)
        return titles


class CompanyCertifiacteInfo(PageData):
    pass


class CompanyBaseInfo(PageData):
    def __init__(self):
        self.majorProduct = None
        self.majorBusiness = None


class CompanyOperateStatus(PageData):
    pass


class CompanyContactInfo(PageData):
    def __init__(self):
        self.contactPerson = None
        self.phoneNumber = None
        self.mobilePhone = None
        self.faxNumber = None
        self.address = None
        self.postcode = None
        self.web = None

    def setContactPerson(self, contactPerson):
        self.contactPerson = contactPerson

    def setPhoneNumber(self, phoneNumber):
        self.phoneNumber = phoneNumber

    def setMobilePhone(self, mobilePhone):
        self.mobilePhone = mobilePhone

    def setFaxNumber(self, faxNumber):
        self.faxNumber = faxNumber

    def setAddress(self, address):
        self.address = address

    def setPostcode(self, postcode):
        self.postcode = postcode

    def setWeb(self, web):
        self.web = web


class Company(object):
    def __init__(self):
        self.companyName = None
        self.url = None

        self.contactInfo = CompanyContactInfo()
        self.operateStatus = CompanyOperateStatus()
        self.baseInfo = CompanyBaseInfo()

    def getTitles(self):
        titles = []
        # for title, value in vars(self).items():
        #     titles.append(title)
        titles.extend(self.contactInfo.getTitles())
        titles.extend(self.baseInfo.getTitles())
        return titles

    def storeSting(self):
        titles, values = self.contactInfo.storeSting()
        tmptitles, tmpvars = self.operateStatus.storeSting()
        titles.extend(tmptitles)
        values.extend(tmpvars)

        tmptitles, tmpvars = self.baseInfo.storeSting()
        titles.extend(tmptitles)
        values.extend(tmpvars)


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
        self.postKeywords = ''
