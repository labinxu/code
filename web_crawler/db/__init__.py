# from functools import total_ordering


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
        return 'varchar(%s) ' % (self.max_length, )


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
            sqlstr = 'create table "%s_table" (' % name
            for name, var in attrs.items():
                if isinstance(var, DBField):
                    sqlstr += '"%s" %s,' % (name, var)
            dct['__sql__'] = '%s);' % sqlstr[:-1]

            return super(ModelBase, cls).__new__(cls,
                                                 name,
                                                 bases,
                                                 dct)


class DBModel(with_metaclass(ModelBase)):
    def __init__(self, *args, **kwargs):
        for name, var in kwargs.items():
            self.__dict__[name] = var

class Myclass(DBModel):
    company_name = CharField(max_length=30)
    company_addr = CharField(max_length=400)
    def dispaly(self):
        print('display')

print(Myclass.__sql__)
my = Myclass(company_name='a', company_addr='aag')
