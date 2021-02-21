import ctypes
from CustomItems import *
ctypes.windll.kernel32.SetConsoleTitleW("PyLine")


class Terminal():
    def __init__(self):
        self.Objects = {}
        self.exc = CustomExceptions()
        self.func = CustomFunctions()
        self.exc.Add("CommandError")
        self.Comms = {}

    def Add(self, name, func_code, bt="static"):
        NewComm = Command(name, func_code, self, bt)
        self.Comms[name] = NewComm
        return NewComm

    def Get(self):
        return self.Comms

    def Delete(self, name):
        if name in self.Comms:
            del self.Comms[name]
            print("Command %s deleted." %name)
        else:
            print("Command %s does not exist" %name)

class func_controller():
    def __init__(self, func_code, build_type, termin):
        self.func_cd = func_code
        self.bt = build_type
        self.term = termin

    def run(self, *params):
        try:
            if len(self.term.func.Get()[self.func_cd]['params']) == len(params):
                self.func_cd(*params)
            else:
                print("The command has too many arguments.")
        except KeyError:
            try:
                self.func_cd(*params)
            except TypeError:
                print('Arguments are incorrect')
           

#define relationships opposite
opposite_rels = {"child": "parent", "parent": "child", "sibling": "sibling"}
class Command():
    def __init__(self, str, func_code, termin, bt):
        self.str = str
        self.term = termin
        self.relations = {}
        self.func_con = func_controller(self.term.func.Get()[func_code], bt, self.term)
        self.term.Objects[str] = {"rels": self.relations, "fnccon": self.func_con}

    def family(self, relt, ostr):
        try:
            self.term.Objects[ostr]["rels"][self.str] = opposite_rels[relt]
            self.relations[ostr] = relt

        except KeyError or TypeError:
             raise self.term.exc.Get()["CommandError"]("You are trying to attach a %s relation type to the unknown Command object %s."%(opposite_rels[relt], ostr))

def call(term, comm):
    item, found, att = 0, False, 0
    comm = comm.split(" ")
    for i in range(0, len(comm)):
        try:
            if (comm[i] in term.Objects.keys() and att == 0) or (comm[i] in term.Objects.keys() and term.Objects[comm[item]]["rels"].get(comm[item + 1]) == "parent"):
                item = i
                found = True
        except IndexError:
            pass
        att += 1
    if not found:
        item = -1

    if comm[item] in term.Objects.keys():
        if not "child" in term.Objects[comm[0]]["rels"].values():
            try:
                term.Objects[comm[item]]["fnccon"].run(*comm[item + 1 if found else len(comm) - 1:])
            except KeyError or IndexError:
                print("Arguments do not work.")
        else:
            print("The command is invalid.")
    else:
        print("The command is invalid.")
    command = input("Command: ")
    call(term, command)

def mf():
    pass


myterm = Terminal()
#funcs
myterm.func.Add("sayhi", "print('HELLO')")
myterm.func.Add("sayhil", "print('hello')")
myterm.func.Add("say", "print(*txt)", params=['*txt'])
myterm.func.Add("mult", "try:\n  print(int(a) * int(b))\n except ValueError:\n  print('This is not a int and an int')", params=['a', 'b'])
myterm.func.Add("geto", "print(objs)", globs={'objs': myterm.Objects})
myterm.func.Add("create", "myterm.func.Add(name, code)", globs={'myterm': myterm}, params=['name', 'code'])
myfunc.func.Add("deffunc", "makefunc()", globs={'makefunc': mf})


myterm.Add("hi", 'sayhi')
myterm.Add("lower", 'sayhil')
myterm.Add("getobjs", 'geto')
myterm.Add("getmults", 'mult')
myterm.Add("says", 'say')
myterm.Get()["hi"].family("parent", "lower")
command = input("Command: ")
call(myterm, command)


