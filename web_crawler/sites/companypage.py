# -*- coding: utf-8 -*-
from sites.pageparser import PageParser


class CompanyPageParser(PageParser):
    def __init__(self, pageurl):
        PageParser.__init__(self, pageurl)
        self.certifInfokeys = ["certificate-ptp ",
                               'certificate-etp ',
                               'certificate ']

    def getCertifyInfoUrl(self):
        soup = self.getSoup()
        if not soup:
            return None

        for key in self.certifInfokeys:
            moreDetail = soup.find('a',
                                   attrs={'class': key})
            if moreDetail:
                break

        return moreDetail.get('href')
