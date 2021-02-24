from types import FunctionType as FT
import contextlib, io

excdata = []
funcdata = {}
func_code = {}
func_prst = {}

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
            func_code[name] = {"code": code, "params": paraglobs['params'] if 'params' in paraglobs else []}
            return NewFunc
        else:
            print("Custom Function %s already exists." %name)

    def AddP(self, name, partst):
        if name in funcdata:
            func_prst[name] = partst
        else:
            print("Custom Function %s does not exist" %name)

    def Get(self):
        return funcdata

    def GetC(self):
        return func_code

    def GetP(self):
        return func_prst

    def Delete(self, name, *args):
        if name in funcdata:
            del funcdata[name]
            del func_code[name]
            del func_prst[name]
            if not args:
                print("Custom Function %s deleted." %name)
        else:
            print("Custom Function %s does not exist" %name)

def raises(func, params):
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            func(*params)
    except Exception as e:
        print(e)
        return True
    else:
        return False