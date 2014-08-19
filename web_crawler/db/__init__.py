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
            print('db name %s' % dbname)
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


class Objects(object):
    Object = type("Object", (), {})

    def __init__(self):
        pass

    @staticmethod
    def transDBRecToObject(dbret, titles):
        result = []
        for item in dbret:
            attrs = dict(zip(titles, item))
            object = Objects.Object()
            object.__dict__.update(attrs)
            result.append(object)
        return result
    
    @staticmethod
    def all():
        sql = 'select * from %s_table' % Objects.__dict__['modelname']
        print(sql)
        dbret = DBHelper.getInstance().select(sql)
        return Objects.transDBRecToObject(dbret, Objects.__dict__['titles'])
        
    def __call__(self):
        print('objects call')

    def filter(self, cond):
        sql = 'select * from %s_table where %s' % (self.name, cond)
        return DBHelper.getInstance().select(sql)


class ModelBase(type):

    objects = Objects()
    
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
        print('tablename %s cls %s ' % (name, cls))
        objattrs = {}
        try:
            objattrs = getattr(Objects, 'modelname')
        except AttributeError:
            objattrs = {}
        finally:
            objattrs.update({name, name})
            setattr(Objects, 'modelname', objattrs)

        sqlstr = 'create table "%s" (' % dct['__table_name__']
        sqlstr += '"id" integer PRIMARY KEY AUTOINCREMENT, '
        titles = ['id']
        for name, var in attrs.items():
            if isinstance(var, DBField):
                titles.append(name)
                sqlstr += '"%s" %s, ' % (name, var)
        dct['__init_table__'] = '%s);' % sqlstr[:-2]
        objattrs = {}
        try:
            objattrs = getattr(Objects, 'titles')
        except AttributeError:
            objattrs = {}
        finally:
            objattrs.update({name, name})
            setattr(Objects, 'titles', titles)
        return super(ModelBase, cls).__new__(cls,
                                             name,
                                             bases,
                                             dct)


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
        print(sqlstr)
        if DBModel.getDBHelper():
            DBModel.getDBHelper().execute(sqlstr)
            if not hasId:
                sqlstr = "select last_insert_rowid()"
                ids = DBModel.getDBHelper().select(sqlstr)
                self.__dict__['id'] = ids[0][0]
        else:
            raise DBException('dbhelper not initial')
