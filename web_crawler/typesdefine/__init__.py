# -*- coding:utf-8-*-
import sys
if '../' not in sys.path:
    sys.path.append('../')

from db import DBModel
from db import CharField


class Enterprise(DBModel):
    company_name = CharField(max_length=50)



ent = Enterprise(company_name='name1')
ent.save()
