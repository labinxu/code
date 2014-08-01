# -*- coding: utf-8 -*-
import sys
if '../' not in sys.path:
    sys.path.append('../')
from sites.pageparser import PageParser


class YellowPageParser(PageParser):
    def __init__(self, pageUrl):
        PageParser.__init__(self, pageUrl)
        self.baseInfoUrl = None
        self.operatestatusUrl = None
        self.contactInfoUrl = None
        
    def _getUrl(self, attrs, urlTag='url'):
        item = self._findItemByAttrs(attrs)
        return item.get('url')
        
    def getBaseInfoUrl(self):
        if self.baseInfoUrl:
            return self.baseInfoUrl
        try:
            attrs = {'class': "companyWeb_BusinessInfo_url"}
            self.baseInfoUrl = self._getUrl(attrs)
            return self.baseInfoUrl
        finally:
            return self.baseInfoUrl

    def getOperateStatusUrl(self):
        if self.operatestatusUrl:
            return self.operatestatusUrl
        try:
            attrs = {'class': 'companyWeb_BusinessInfo_url'}
            self.operatestatusUrl = self._getUrl(attrs)
            return self.operatestatusUrl
        finally:
            return self.operatestatusUrl

    def getContactInfoUrl(self):
        if self.contactInfoUrl:
            return self.contactInfoUrl
        try:
            attrs = {'class': 'companyWeb_contact_url'}
            self.contactInfoUrl = self._getUrl(attrs)
            return self.contactInfoUrl
        finally:
            return self.contactInfoUrl
