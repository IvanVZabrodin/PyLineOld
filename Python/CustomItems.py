from types import FunctionType as FT

excdata = []
funcdata = {}

class CustomExceptions():
    def __init__(self):
        pass

    def Add(self, name):
        class NewException(Exception):
            def __init__(self, m):
                self.message = m
            def __str__(self):
                return self.message
        NewException.__name__ = name

        if not NewException in excdata:
            excdata.append(NewException)
            return NewException
        else:
            print("Exception Error %s already exists." %name)
        
    def Get(self):
        return {Exce.__name__:Exce for Exce in excdata}

    def Delete(self, name):
        if name in excdata:
            del excdata[name]
            print("Custom Exception %s deleted." %name)
        else:
            print("Custom Exception %s does not exist" %name)

class CustomFunctions():
    def __init__(self):
        pass

    def Add(self, name, code, **paraglobs):
        NewCode = compile("""def """+name+"""("""+(', '.join(paraglobs['params']) if 'params' in paraglobs else "")+"""):\n """+str(code), name, "exec")
        NewFunc = FT(NewCode.co_consts[0], (({**paraglobs['globs'], **globals()} if 'globs' in paraglobs else globals())), name)
        if not name in funcdata:
            funcdata[name] = NewFunc
            return NewFunc
        else:
            print("Custom Function %s already exists." %name)

    def Get(self):
        return funcdata

    def Delete(self, name):
        if name in funcdata:
            del funcdata[name]
            print("Custom Function %s deleted." %name)
        else:
            print("Custom Function %s does not exist" %name)