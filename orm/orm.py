from datastore import ds
import datetime, hmac
    

class Property(object):
    """Top Level Class that describes a generic property that stores a value.
    It has three methods, a getter and a setter for the value, as well as a method return a new object of
    type Property"""
    def __init__(self,PrimaryKey=False):
        """Initiates the property and sets whether this is the primary key property or not."""
        self._primarykey = PrimaryKey
        self._val = ''
    
    def getval(self):
        """Returns the value of _val"""
        return self._val
    
    def setval(self, value):
        """Sets the value of _val"""
        self._val = value
    
    def adhoc(self):
        """Returns a new object of the same type as the calling object."""
        k = self.__class__
        return k()

class IntegerProperty(Property):
    """A subclass of property that holds an Integer value instead of a generic value."""
    def setval(self, value):
        if isinstance(value,int):
            self._val = value
        else:
            raise TypeError
    
    #val = property(getval,setval)

class StringProperty(Property):
    """A subclass of property that holds an String value instead of a generic value."""
    def setval(self, value):
        if isinstance(value,str) or isinstance(value,unicode):
            self._val = str(value)
        else:
            raise TypeError

class DateTimeProperty(Property):
    """A subclass of property that holds an datetime value instead of a generic value."""
    pass

class ModelQuery(object):
    
    def __init__(self, cls):
        self._filters = []
        self._order = ''
        self._tablename = cls.__name__
        self._class = cls
    
    def filter(self, property_op, value):
        self._filters.append("%s %s"%(property_op,value))
        
    
    def order(self, column):
        """Sets order to return objects in."""
        if column[0] == '-':
            self._order = '%s DESC'%column[1:]
        else:
            self._order = '%s ASC'%column
    
    def execute(self):
        _where = ' and '.join(self._filters)
        if not _where:
            _where = None
        ckey = self._class.makekey(''.join([self._tablename,''.join(self._filters), self._order]))
        #print ckey
        values = ds.get(self._tablename, ckey)
        if values is None:
            values = ds.select(self._tablename,where=_where,order=self._order)
            if values:
                values = [self._class.make(x) for x in values]
                ds.set(self._tablename, ckey, values)
        
        return values


class Model(object):
    """Model object is the top level class upon which all Model Classes inherit."""
    processed = False
    
    def getval(self, n):
        """Returns the value of object named <n> from the properties dictionary."""
        return self.properties[n].getval()
    
    def setval(self, n, value):
        """Sets the value of object named <n> from the properties dictionary."""
        self.properties[n].setval(value)
    
    def __new__(cls, *args, **kwargs):
        """Overloads the __new__ function to updated the class with
        properties defined in a subclass of Model."""        
        obj = super(type(cls), cls).__new__(cls)
        # checks whether or not the properties defined in the subclass have been created yet.
        if not cls.processed:
            # for all objects in __dict__ if it is an instance of Property (defined in subclass)
            # creates a property (getters, setters) for the named property, and hides the original
            # Property Objects.
            for k,v in cls.__dict__.items():
                if isinstance(v,Property):
                    if v._primarykey:
                        cls.primarykey = k
                    if k[0] == "_":
                        n = k[1:]
                    else:
                        #print "First Time Creating object saves class objects to _%s."%k
                        n = k
                        h = "_%s"%k
                        setattr(cls,h,v)
                        # generates the functions to call for getter/setter as we need more information
                        # than the basic getter/setter provides we pass these to make custom functions.
                        setattr(cls,n,property(obj.make_getter(obj,n),obj.make_setter(obj,n)))
            cls.processed = True
        
        
        return obj
        
    
    def __init__(self):
        """Gets tablename to match Class name and creates properties dictionary to hold properties."""
        self.__tablename__ = self.__class__.__name__
        cls = self.__class__
        self._primarykey = cls.primarykey
        
        self.properties = { k[1:]: v.adhoc() for k,v in cls.__dict__.items() if isinstance(v,Property) }
        
        
    def make_getter(self, obj, n):
        """Makes and returns a getter function."""
        return lambda self: self.getval(n)
    
    def make_setter(self, obj, n):
        """Makes and returns a setter function."""
        return lambda self, value: self.setval(n,value)

    def display(self):
        """Displays property value pairs one to a row."""
        for k,v in self.properties.items():
            print '%s : %s'%(k,v.getval())
        print
    
    @classmethod
    def makekey(cls,value):
        "Makes a key value for the cache store."
        secret = 'jfkl;aNNdip[10[98dfnl;a&fnfnip-1nvmcal;f8bjgls8dg]99anc]'
        newkey = hmac.new(secret, value).hexdigest()
        return newkey
    
    @classmethod
    def make(cls,value):
        result = cls()
        for p,v in result.properties.items():
            #print type(value[p]), p
            v.setval(value[p])
            #result.__setattr__(p,value[p])
        return result
    
    @classmethod
    def fetch(cls,key):
        # look for key in cache
        result = cls()
        value = ds.get(result.__tablename__,key)
        # if not found in cache, check database
        if value is None:
            if key == 'all':
                _where = None
            else:
                _where = '%s="%s"'%(cls.primarykey,key)
            value = ds.select(result.__tablename__,where=_where).list()
            # if in database add value to cache
            if value:
                ds.set(result.__tablename__,key,value)
        
        return value
    
    @classmethod
    def bykey(cls, key):
        result = cls.fetch(key)
        if isinstance(result,cls):
            return result
        if result and len(result) == 1:
            return cls.make(result[0])
        
        return None

    @classmethod
    def all(cls):
        q = ModelQuery(cls)
        return q
            
            
    def put(self):
        props = {k:v.getval() for k,v in self.properties.items()}
        if self.__class__.fetch(self.getval(self._primarykey)):
            ds.update(self.__tablename__,where='%s=%s'%(self._primarykey,self.getval(self._primarykey)),**props)
        else:
            del props[self._primarykey]
            rowid = ds.insert(self.__tablename__,**props)
            self.setval(self._primarykey,rowid)
        
        ds.set(self.__tablename__,self.getval(self._primarykey),self)
        return self.getval(self._primarykey)

    def remove(self):
        ds.delete(self.__tablename__,where='%s=%s'%(self._primarykey,self.getval(self._primarykey)))
    
    
