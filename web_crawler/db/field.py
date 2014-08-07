# -*- coding:utf-8-*-


class Field(object):
    def __init__(self, name=None, max_length=None):
        self.name = name
        self.max_length = max_length

    def __str__(self):
        tmp = ''
        for name, var in vars(self).items():
            strt = '%s,' % var
            tmp += strt
        return tmp


class MyObj(object):
    field = Field(name='companyName', max_length=200)

    def __init__(self):
        pass

    def __str__(self):
        return str(self.field)

print(MyObj())
