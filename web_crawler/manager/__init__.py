# from functools import total_ordering
import sqlite3
import sys
if '../' not in sys.path:
    sys.path.append('../')


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
            pass
            DBHelper._instance = DBHelper(dbname)
        return DBHelper._instance

    def __init__(self, dbname):
        super(DBHelper, self).__init__(dbname)

    @staticmethod
    def reset(dbname):
        DBHelper._instance = DBHelper(dbname)


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


def transDBRecToObject(dbret, titles):
    result = []
    for item in dbret:
        attrs = dict(zip(titles, item))
        object = type('object', (), {})()
        object.__dict__.update(attrs)
        result.append(object)
    return result


def all(cls):
    def all():
        titles = ''
        for t in cls.titles:
            titles += '%s,' % t
        sql = 'select %s from %s_table' % (titles[:-1], cls.modelname)
        dbret = DBHelper.getInstance().select(sql)
        return transDBRecToObject(dbret, cls.titles)
    return all()


def filter(cls, cond):
    def filter():
        titles = ''
        for t in cls.titles:
            titles += '%s,' % t
        sql = 'select %s from %s_table where %s' % (titles[:-1],
                                                    cls.modelname,
                                                    cond)
        dbret = DBHelper.getInstance().select(sql)
        return transDBRecToObject(dbret, cls.titles)
    return filter()
                                            

class ModelBase(type):
    typeMap = {}

    def __new__(cls, name, bases, dct):
        super_new = super(ModelBase, cls).__new__
        if (name == 'NewBase' and dct == {}) or name == 'DBModel':
            return super_new(cls, name, bases, dct)

        attrs = dict((n, value) for n,
                     value in dct.items() if not n.startswith('__'))

        dct['__table_name__'] = '%s_table' % name
        sqlstr = 'create table "%s" (' % dct['__table_name__']
        sqlstr += '"id" integer PRIMARY KEY AUTOINCREMENT, '
        titles = ['id']
        for n, var in attrs.items():
            if isinstance(var, DBField):
                titles.append(n)
                sqlstr += '"%s" %s, ' % (n, var)

        dct['__init_table__'] = '%s);' % sqlstr[:-2]

        tmptype = type('Obj%s' % name, (), {})

        setattr(tmptype, 'modelname', name)
        setattr(tmptype, 'titles', titles)
        setattr(tmptype,
                'all',
                classmethod(all))
        setattr(tmptype,
                'filter',
                classmethod(filter))

        ModelBase.typeMap[name] = tmptype

        return super(ModelBase, cls).__new__(cls,
                                             name,
                                             bases,
                                             dct)


class DBModel(with_metaclass(ModelBase)):

    @classmethod
    def objects(cls):
        def ob():
            return cls.typeMap[cls.__name__]
        return ob()

    @staticmethod
    def getDBHelper():
        try:
            return DBHelper.getInstance()
        except Exception as e:
            pass

    def __init__(self, *args, **kwargs):
        for name, var in kwargs.items():
            self.__dict__[name] = var

    def save(self):
        attrs = dict((name, value) for name,
                     value in self.__dict__.items()
                     if not name.startswith('__'))
        titles = ''
        values = ''
        hasId = False
        sqlstr = ''
        if 'id' in self.__dict__.keys():
            sqlstr = 'update %s set ' % self.__table_name__
            for title, var in attrs.items():
                if not title == 'id':
                    titles += '%s="%s", ' % (title, var)
            titles = titles[:-2]
            titles += ' where id=%s' % self.__dict__['id']
            sqlstr += titles
            hasId = True
        else:
            sqlstr = 'insert into %s(%s) values(%s)'
            for title, var in attrs.items():
                titles += '%s, ' % title
                values += '"%s", ' % var

            sqlstr = sqlstr % (self.__table_name__,
                               titles[:-2], values[:-2])

        if DBModel.getDBHelper():
            DBModel.getDBHelper().execute(sqlstr)
            if not hasId:
                sqlstr = "select last_insert_rowid()"
                ids = DBModel.getDBHelper().select(sqlstr)
                self.__dict__['id'] = ids[0][0]
        else:
            raise DBException('dbhelper not initial')
