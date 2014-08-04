# -*- coding: utf-8 -*-
import sys
if '../' not in sys.path:
    sys.path.append('../')
from sites.pageparser import PageParser
from typesdefine.data_types import CompanyContactInfo


class ContactInfoPageParser(PageParser):
    def __init__(self, pageUrl):
        PageParser.__init__(self, pageUrl)
        self.contactInfo = None
        self.contentsMapping = {}

    def initContentsMapping(self):
        self.contactInfo = CompanyContactInfo()
        self.contentsMapping = {3: self.contactInfo.setContactPerson,
                                5: self.contactInfo.setPhoneNumber,
                                7: self.contactInfo.setMobilePhone,
                                9: self.contactInfo.setFaxNumber,
                                11: self.contactInfo.setAddress,
                                13: self.contactInfo.setPostcode,
                                15: self.contactInfo.setWeb}

    def _setContactInfo(self, index, var):
        if index in self.contentsMapping.keys():
            self.contentsMapping[index](var)

    def _getContentTable(self):
        soup = self.getSoup()
        if not soup:
            return None

        contents = soup.find_all('div', attrs={'class': "content"})
        for content in contents:
            item = content.find('table')
            if item:
                return item

    def getContactInfo(self):
        if self.contactInfo:
            return self.contactInfo
        self.initContentsMapping()
        table = self._getContentTable()
        if not table:
            return None

        for index, item in enumerate(table.find_all('td')):
            self._setContactInfo(index, item.text.expandtabs(1).strip())
        return self.contactInfo
