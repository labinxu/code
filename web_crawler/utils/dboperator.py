# -*- coding: utf-8 -*-
import sqlite3


class DBOperator(object):
    def __init__(self, dbname):
        self.db = sqlite3.connect(dbname)

    def execute(self, sql):
        cursor = self.db.cursor()
        cursor.execute(sql)
        self.db.commit()

    def select(self, sql):
        cursor = self.db.cursor()
        cursor.execute(sql)
        return cursor.fetchall()

    def getdb(self):
        return self.db
