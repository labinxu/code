# -*- coding:utf-8-*
from utils import CommandLine
from db import DBHelper
from typesdefine import Enterprise
import importlib
import os


# class WebPage(object):
#     def __init__(self, url):
#         self.pageName = ''
#         self.url = url
#         self.validSearchItems = []
#         self.parser = None


# def matchAUrl(text):
#     urlpatern = '.*(http.+htm)'
#     return re.match(urlpatern, text).group(1)


# def taobao_main(url):
#     response = request.urlopen(url)
#     html = response.read()
#     data = html.decode('gbk').encode('utf-8')
#     soup = BeautifulSoup(data)
#     webPage = WebPage(url)
#     webPage.pageName = 'taobao'
#     for list in soup.find_all('form'):
#         for itemli in list.find_all('li'):
#             dataConf = itemli.get('data-config')
#             item = itemli.find('a')
# webPage.validSearchItems.append((item.string,
# matchAUrl(dataConf)))
#         break

#     print(str(webPage.validSearchItems))

def CreateTask(taskName=None):
    if taskName:
        dbname = '%s.db' % taskName
        if os.path.exists(dbname):
            dbhelper = DBHelper.getInstance(dbname)
        else:
            dbhelper = DBHelper.getInstance(dbname)
            dbhelper.execute(Enterprise.__init_table__)


def GetSiteParser(siteName):
    module = importlib.import_module('sites.%s.main' % siteName)
    return module.GetParser()


def main():
    cmdline = CommandLine()
    args, _ = cmdline.parseCmdLine()
    try:
        CreateTask(args.TASKNAME)
        GetSiteParser(args.WEBSITE).startTask(product=args.PRODUCT,
                                              supplier=args.SUPPLIER)
    except Exception as e:
        print(str(e))


if __name__ == '__main__':
    main()
