# from functools import total_ordering
import sqlite3


class DBException(Exception):
    def __init__(self, msg):
        self.msg = msg


def with_metaclass(meta, *bases):
    """Create a base class with a metaclass."""
    return meta("NewBase", bases, {})


class Empty(object):
    pass


class NOT_PROVIDED:
    pass


class DBField(object):
    """Base class for all field types"""
    def __init__(self, name=None, max_length=None, default=NOT_PROVIDED):
        self.name = name
        self.max_length = max_length


class CharField(DBField):
    def __init__(self, *args, **kwargs):
        super(CharField, self).__init__(*args, **kwargs)
        # self.validators.append(validators.MaxLengthValidator(self.max_length))

    def __str__(self):
        return 'varchar(%s) ' % self.max_length


class ModelBase(type):
        def __new__(cls, name, bases, dct):
            super_new = super(ModelBase, cls).__new__
            if name == 'NewBase' and dct == {}:
                return super_new(cls, name, bases, dct)
                parents = [b for b in bases if isinstance(b, ModelBase) and
                           not (b.__name__ == 'NewBase' and
                                b.__mro__ == (b, object))]
                if not parents:
                    return super_new(cls, name, bases, dct)
            attrs = dict((name, value) for name,
                         value in dct.items() if not name.startswith('__'))
            dct['__table_name__'] = '%s_table' % name

            sqlstr = 'create table "%s" (' % dct['__table_name__']

            for name, var in attrs.items():
                if isinstance(var, DBField):
                    sqlstr += '"%s" %s, ' % (name, var)
            dct['__init_table__'] = '%s);' % sqlstr[:-2]
            return super(ModelBase, cls).__new__(cls,
                                                 name,
                                                 bases,
                                                 dct)


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


class DBHelper(DBOperator):
    _instance = None

    @staticmethod
    def getInstance(dbname=None):
        if not DBHelper._instance:
            print('db name %s' % dbname)
            DBHelper._instance = DBOperator(dbname)
        return DBHelper._instance

    @staticmethod
    def reset():
        DBHelper._instance = None


class DBModel(with_metaclass(ModelBase)):

    @staticmethod
    def getDBHelper():
        try:
            return DBHelper.getInstance()
        except Exception as e:
            print('get DB helper error %s' % str(e))

    def __init__(self, *args, **kwargs):
        for name, var in kwargs.items():
            self.__dict__[name] = var

    def save(self):
        attrs = dict((name, value) for name,
                     value in self.__dict__.items()
                     if not name.startswith('__'))
        sqlstr = 'insert into %s(%s) values(%s)'
        titles = ''
        values = ''
        for title, var in attrs.items():
            titles += '%s, ' % title
            values += '"%s", ' % var
        sqlstr = sqlstr % (self.__table_name__,
                           titles[:-2], values[:-2])
        # print(DBModel.getDBHelper())
        if DBModel.getDBHelper():
            DBModel.getDBHelper().execute(sqlstr)
        else:
            print('error')
            raise DBException('dbhelper not initial')
