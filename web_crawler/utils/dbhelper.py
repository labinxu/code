# -*- coding: utf-8 -*-
import sys
if '../' not in sys.path:
    sys.path.append('../')
from utils.dboperator import DBOperator


class DBHelper(DBOperator):
    def __init__(self, dbname):
        DBOperator.__init__(self, dbname)
