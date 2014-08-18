# -*- coding:utf-8-*-
import sys
if '../' not in sys.path:
    sys.path.append('../')

from db import DBModel
from db import CharField


class Enterprise(DBModel):
    company_name = CharField(max_length=100)
    company_phone_number = CharField(max_length=20)
    company_contacts = CharField(max_length=10)
    company_mobile_phone = CharField(max_length=20)
    company_fax = CharField(max_length=10)
    company_postcode = CharField(max_length=10)
    company_website = CharField(max_length=100)
    company_addr = CharField(max_length=100)
    company_details = CharField(max_length=200)


class Task(DBModel):
    task_name = CharField(max_length=20)
    task_search_words = CharField(max_length=20)
    task_site_name = CharField(max_length=10)
    task_web_url = CharField(max_length=100)
    task_status = CharField(max_length=2)
