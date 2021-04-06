import types, string
from os import system
from Python.CustomItems import *
system("title " + "PyLine")

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

    def Delete(self, name, *args):
        if name in self.Comms:
            del self.Comms[name]
            if not args:
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
opposite_rels = {"child": "parent", "parent": "child"}
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
             #raise self.term.exc.Get()["CommandError"]("You are trying to attach a %s relation type to the unknown Command object %s."%(opposite_rels[relt], ostr))
             print("You are trying to attach a %s relation type to the unknown Command object %s."%(opposite_rels[relt], ostr))
             return

def call(term, comm):
    item, found, overfound = 0, False, True
    comm = comm.split(" ")
    for i in range(0, len(comm)):
        try:
            if (comm[i] in term.Objects.keys() and i == 0) or (comm[i] in term.Objects.keys() and term.Objects[comm[item]]["rels"].get(comm[item + 1]) == "parent"):
                item = i
                found = True
        except IndexError:
            pass
        except KeyError:
            if i == 0:
                print("The command is invalid.")
                overfound = False
    if comm[item] in term.Objects.keys() and overfound:
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

def inp(lines, pasa, inc):
    global l
    line = input("-"+("-------" if l == 0 else "line:%s"%l if l > 9 else "line:%s-"%l)+"--> ")
    if line.replace(" ", "")[0:2] == "||":
        lc = line.split(" ")
        if lc[0][2:] == "line" and lc[1].isdigit() and int(lc[1]) <= len(lines):
            l = int(lc[1])
        if lc[0][2:] == "code":
            print(*lines)
        if lc[0][2:] == "exit":
            lines.extend(["", " \n", " \n"])
            return False
        if lc[0][2:] == "paras":
            pasa()
    elif l != 0:
        lines[l - 1] = (" " if l != 1 else "") + line + "\n"
        l = 0
    elif l == 0:
        lines.append(" " + line + "\n")



def funcmake(name, *paras):
    if name in active_term.func.Get().keys():
        print("Function %s already exists."%name)
        return
    lins = []
    paras = list(paras)
    l = 0
    parastest = []
    brk = False
    def parastart():
        if paras:
            for para in paras:
                if set(para).difference(string.ascii_letters + string.digits + '*'):
                    print("Symbols not supported")
                    brk = True
                    return
                elif para[0] == "*":
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
                    brk = True
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
                else:
                    spec = input("%s|Value: "%(para))
                    if spec == "||stop":
                        stop = True
                    else:
                        print("In the error check %s will be %s."%(para, spec))
                        parastest.append(spec)
    parastart()
    if brk:
        return
    def useless():
        pass
    
    incorrect = True
    r = 0
    while incorrect:
        r += 1
        while lins[-2:].count(" \n") < 2:
            i = inp(lins, useless, incorrect)
            if i == False:
                incorrect = i
        if not "" in lins:
            if r == 1: lins[0] = lins[0][1:]
            NC = compile("def "+name+"("+(', '.join(paras) if paras else "")+"):\n "+''.join(lins[:-2]), name, "exec")
            NF = types.FunctionType(NC.co_consts[0], globals(), name)
            if raises(NF, parastest):
                print("Error, please try again.")
                lins = lins[:-2]
                continue
            else:
                active_term.func.Add(str(name + "M"), ''.join(lins[:-2]), params=paras)
                active_term.Add(name, str(name + "M"))
                active_term.func.AddP(str(name + "M"), parastest)
                incorrect = False





def funcedit(name):
    if not name + "M" in active_term.func.Get().keys():
        print("Function %s does not exist."%name)
        return
    paras = active_term.func.GetC()[name + "M"]["params"]
    parastest = active_term.func.GetP()[name + "M"]
    def parag():
        pars = input("Parameters: ")
        nonlocal paras, parastest
        oldpt = parastest
        del parastest[:]
        oldp = paras
        paras = pars.split(" ")
        for para in paras:
            if set(para).difference(string.ascii_letters + string.digits + '*'):
                print("Symbols not supported")
                paras = oldp
                parastest = oldpt
                return
            elif para[0] == "*":
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
            else:
                spec = input("%s|Value: "%(para))
                if spec == "||stop":
                    stop = True
                else:
                    print("In the error check %s will be %s."%(para, spec))
                    parastest.append(spec)
    lins = [active_term.func.GetC()[name + "M"]["code"]]
    print(lins, paras)
    incorrec = True
    while incorrec:
        while lins[-2:].count(" \n") < 2:
            i = inp(lins, parag, incorrec)
            print(paras)
            if i == False:
                incorrec = i
        if not "" in lins:
            NC = compile("def "+name+"("+(', '.join(paras) if paras else "")+"):\n "+''.join(lins[:-2]), name, "exec")
            NF = types.FunctionType(NC.co_consts[0], globals(), name)
            if raises(NF, parastest):
                print("Error, please try again.")
                lins = lins[:-2]
                continue
            else:
                active_term.func.Delete(str(name + "M"), True)
                active_term.Delete(name, True)
                active_term.func.Add(str(name + "M"), ''.join(lins[:-2]), params=paras)
                active_term.Add(name, name + "M")
                active_term.func.AddP(name + "M", parastest)
                incorrec = False

myterm = Terminal()
#funcs
#with open('funcs.txt', )

myterm.func.Add("sayhi", "print('HELLO')")
myterm.func.Add("sayhil", "print('hello')")
myterm.func.Add("say", "print(*txt)", params=['*txt'])
myterm.func.Add("mult", "try:\n  print(int(a) * int(b))\n except ValueError:\n  print('This is not a int and an int')", params=['a', 'b'])
myterm.func.Add("geto", "print(objs)", globs={'objs': myterm.Objects})
myterm.func.Add("fam", "if fmt in opposite_rels.keys():\n  objs.Get()[comm].family(fmt, comm1)\n else:\n  print('No such family type')", globs={'opposite_rels': opposite_rels, 'objs': myterm}, params=['comm', 'fmt', 'comm1'])

myterm.Add("hi", 'sayhi')
myterm.Add("lower", 'sayhil')
myterm.Add("getobjs", 'geto')
myterm.Add("getmults", 'mult')
myterm.Add("says", 'say')
myterm.Add("create", funcmake)
myterm.Add("edit", funcedit)
myterm.Add("family", 'fam')
myterm.Get()["hi"].family("parent", "lower")

command = input("Command: ")

call(myterm, command)