from functools import total_ordering


class Empty(object):
    pass


class NOT_PROVIDED:
    pass


class DBField(object):
    """Base class for all field types"""
    def __init__(self, name=None, max_length=None):
        self.name = name
        self.max_length = max_length

    def __str__(self):
        pass


class CharField(DBField):
    def __init__(self, *args, **kwargs):
        super(CharField, self).__init__(*args, **kwargs)
        # self.validators.append(validators.MaxLengthValidator(self.max_length))


class Myclass(object):
    name = CharField(max_length=30)

    def displayAttributes(self):
        for name, value in vars(self).items():
            print('%s = %s' % (type(name), type(value)))
    

if __name__ == '__main__':
    myObj = Myclass()
    myObj.displayAttributes()
