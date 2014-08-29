# -*- coding:utf-8-*-
import xlwt3


class PyExcel(object):
    def __init__(self, filename, tabmap, titls, objects, sheetName='sheet1'):
        self.filename = filename
        self.title = titls
        self.tabmap = tabmap
        self.objects = objects
        self.sheetName = sheetName

    def _fillExcel(self, sheet, objects):
        for row, ent in enumerate(objects):
            for name, var in vars(ent).items():
                sheet.write(row, self.tabmap[name], var)

    def save(self):
        wb = xlwt3.Workbook()
        sheet = wb.add_sheet(self.sheetName)
        self
        for col, title in enumerate(self.title):
            sheet.write(0, col, title)

        self._fillExcel(sheet, self.data)
        wb.save(self.filename)
