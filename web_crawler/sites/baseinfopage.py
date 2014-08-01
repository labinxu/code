# -*- coding: utf-8 -*-
import sys
if '../' not in sys.path:
    sys.path.append('../')
from sites.pageparser import PageParser
from typesdefine.data_types import CompanyBaseInfo


class BaseInfoPageParser(PageParser):
    def __init__(self, pageUrl):
        PageParser.__init__(self, pageUrl)
        self.companyBaseInfo = CompanyBaseInfo()

    def getBaseInfo(self):
        if self.companyBaseInfo:
            return self.companyBaseInfo
        
        try:
            # self.getSoup().
            pass
        finally:
            pass
            
