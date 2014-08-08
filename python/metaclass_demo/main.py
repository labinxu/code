def make_hook(f):
    f.is_hook = 1
    return f


class MyType(type):
    def __new__(cls, name, bases, attrs):
        if name.startswith('None'):
            return None

        newattrs = {}
        for attrname, attrvalue in attrs.items():
            print(attrname)
            if getattr(attrvalue, 'is_hook', 0):
                newattrs['__%s__' % attrname] = attrvalue
            else:
                newattrs[attrname] = attrvalue

        return super(MyType, cls).__new__(cls, name, bases, newattrs)

    def __init__(self, name, bases, attrs):
        super(MyType, self).__init__(name, bases, attrs)
        print('Would register class %s now' % self)
    
    def __add__(self, other):
        class AutoClass(self, other):
            pass
        return AutoClass

    def unregister(self):
        print('would unregister class %s now' % self)


class MyObject:
    __metaclass__ = MyType


class NoneSample(MyObject):
    pass


# print(type(NoneSample), repr(NoneSample))


class Example(MyObject):
    def __init__(self, value):
        self.value = value
    
    @make_hook
    def add(self, other):
        return self.__class__(self.value + other.value)

# Example.unregister()
inst = Example(10)
# inst.unregister()
###################################


class Field(object):
    def __init__(self, max):
        self.max_length = max


def with_metaclass(meta, *bases):
    """Create a base class with a metaclass."""
    return meta("NewBase", bases, {})


class UpperAttrMetaclass(type):
    def __new__(cls, name, bases, dct):
        attrs = ((name, value) for name,
                 value in dct.items() if not name.startswith('__'))

       # uppercase_attr = dict((name.upper(), value) for name, value in attrs)
        #for name , var in dict(attrs):
        #    print(name)
         #   print(var.max_length)
        
        return super(UpperAttrMetaclass, cls).__new__(cls,
                                                      name,
                                                      bases,
                                                      dict(attrs))


class MyObject(with_metaclass(UpperAttrMetaclass, object)):
    pass


class Concreate(MyObject):
    field1 = Field(max=10)
    field2 = Field(max=20)

print(hasattr(Concreate,'FIELD1'))
print(hasattr(Concreate,'field1'))
