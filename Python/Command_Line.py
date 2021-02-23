import ctypes, types, string
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

active_term = Terminal()

class func_controller():
    def __init__(self, func_code, build_type, termin):
        self.func_cd = func_code
        self.bt = build_type
        self.term = termin

    def run(self, *params):
        global active_term
        active_term = self.term
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
        self.func_con = func_controller(self.term.func.Get()[func_code] if not callable(func_code) else func_code, bt, self.term)
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

l = 0

def inp(lines):
    global l
    line = input("-"+("-------" if l == 0 else "line:%s"%l if l > 9 else "line:%s-"%l)+"--> ")
    if line.replace(" ", "")[0:2] == "||":
        lc = line.split(" ")
        if lc[0][2:] == "line" and lc[1].isdigit() and int(lc[1]) <= len(lines):
            l = int(lc[1])
        if lc[0][2:] == "code":
            print(*lines)
        if lc[0][2:] == "exit":
            lines.append("")
            lines.extend(["\n", "\n"])
    elif l != 0:
        lines[l - 1] = " " + line + "\n"
        l = 0
    elif l == 0:
        lines.append(line + "\n")


def funcmake(name, *paras, **kwargs):
    lins = likwargs["lines"] if "lines" in kwargs else []
    paras = list(paras)
    l = 0
    parastest = []
    if paras:
        for para in paras:
            if para[0] == "*":
                stop = False
                run = 1
                while not stop:
                    spec = input("%s|%s|Value: "%(para, run))
                    if spec == "||stop":
                        stop = True
                    else:
                        print("In the error check item %s in %s will be %s."%(run, para, spec))
                        parastest.append(spec)
                        run += 1
            elif "**" in para:
                print("Kwargs are not supported yet.")
                return
                #stop = False
                #run = 1
                #while not stop:
                #    speck = input("%s|%s|Keyword: "%(para, run))
                #    specv = input("%s|%s|Value: "%(para, speck))

                #    if "||stop" in [speck, specv]:
                #        stop = True
                #    else:
                #        print("In the error check %s in %s will be %s."%(speck, para, specv))
                #        parastest.append()
                #        run += 1
            elif any(not char in para for char in list(string.ascii_letters)):
                print("Symbols not supported")
                return
            else:
                spec = input("%s|Value: "%(para))
                if spec == "||stop":
                    stop = True
                else:
                    print("In the error check %s will be %s."%(para, spec))
                    parastest.append(spec)

    def inpi():
        while lins[-2:].count("\n") < 2:
            inp(lins)
    inpi()
    if not "" in lins:
        NC = compile("def "+name+"("+(', '.join(paras) if paras else "")+"):\n "+''.join(lins[:-2]), name, "exec")
        NF = types.FunctionType(NC.co_consts[0], globals(), name)
        if raises(NF, parastest):
            print("Error, please try again.")
            del lins[-2:]
            inpi()
        else:
            print(paras)
            active_term.func.Add(str(name + "M"), ''.join(lins[:-2]), params=paras)
            active_term.Add(name, str(name + "M"))

myterm = Terminal()
#funcs
myterm.func.Add("sayhi", "print('HELLO')")
myterm.func.Add("sayhil", "print('hello')")
myterm.func.Add("say", "print(*txt)", params=['*txt'])
myterm.func.Add("mult", "try:\n  print(int(a) * int(b))\n except ValueError:\n  print('This is not a int and an int')", params=['a', 'b'])
myterm.func.Add("geto", "print(objs)", globs={'objs': myterm.Objects})

myterm.Add("hi", 'sayhi')
myterm.Add("lower", 'sayhil')
myterm.Add("getobjs", 'geto')
myterm.Add("getmults", 'mult')
myterm.Add("says", 'say')
myterm.Add("create", funcmake)
myterm.Get()["hi"].family("parent", "lower")

command = input("Command: ")

call(myterm, command)