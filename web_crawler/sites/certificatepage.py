# -*- coding: utf-8 -*-
from sites.pageparser import PageParser


class CertifiactePageParser(PageParser):
    def __init__(self, pageurl):
        PageParser.__init__(self, pageurl)
        self.yellowpageUrl = None

    def getYellowPageUrl(self):
        if self.yellowpageUrl:
            return self.yellowpageUrl
        
        linkitem = self.getSoup().find('a', attrs={'class': 'comment-link'})
        if linkitem:
            self.yellowpageUrl = linkitem.get('href')

        return self.yellowpageUrl
