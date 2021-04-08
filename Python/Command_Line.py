import types, string
import os, sys
from CustomItems import *
from PyMation.files import *
os.system("title " + "PyLine")

class Terminal():
    def __init__(self, name):
        self.Objects = {}
        self.exc = CustomExceptions()
        self.func = CustomFunctions()
        self.exc.Add("CommandError")
        self.Comms = {}
        self.f = Pfile(name + "funcsave.datr", os.path.dirname(os.path.realpath(__file__)))
        famsneeded = {}
        curfunc = []
        paras = []
        fams = {}
        fam, para = False, False
        fn = ""
        n = ""
        disl = 0
        for ind, line in enumerate(self.f.load()):
            print(disl)
            if line == '------------------\n':
                #structure is myterm.func.Add("sayhi", "print('HELLO')")
                self.func.Add(fn, ''.join(curfunc), params=paras)
                nc = self.Add(n, fn, w=False, l=disl)
                famsneeded[n] = fams
                fam, para, fams, paras, curfunc = False, False, {}, [], []
                disl = ind + 1
                print(n + " " + str(nc.l))
            elif line[:6] == "|name:":
                n = line[6:-1]
            elif line[:7] == "|fname:":
                fn = line[7:-1]
            elif line == "|params:\n":
                para, fam = True, False
            elif line == "|rels:\n":
                fam, para = True, False
            else:
                if para:
                    paras.append(line[:-1])
                elif fam:
                    fams[line.split()[0]] = line.split()[1]
                else:
                    curfunc.append(line)
        for nam, famn in famsneeded.items():
            for obj, r in famn.items():
                self.Comms[nam].family(obj, r)
                

    def Add(self, name, func_code, bt="static", w=True, l=-1):
        if l == -1:
            l = len(self.f.load())
        NewComm = Command(name, func_code, self, bt, l, w)
        self.Comms[name] = NewComm
        if func_code in self.func.Get().keys() and bt != "globular" and w:
            self.f.write("|name:" + name, "|fname:" + func_code, self.func.GetC()[func_code]["code"], "|params:", *self.func.GetC()[func_code]["params"], "|rels:", "------------------")
        return NewComm

    def Get(self):
        return self.Comms

    def Delete(self, name, pr=True):
        if name in self.Comms:
            c = self.Comms[name]
            del self.Objects[name]
            lenf = self.f.load().index('------------------\n', self.Comms[name].l)
            self.f.clear(*range(self.Comms[name].l, lenf + 1))
            lend = lenf + 1 - self.Comms[name].l
            del self.Comms[name]
            for comm in self.Comms.values():
                if name in comm.relations.keys():
                    del comm.relation[name]
                    del self.Objects[comm.str]["rels"][name]
                if comm.l >= c.l:
                    comm.l -= lend
            if pr:
                print("Command %s deleted." %name)
        else:
            print("Command %s does not exist" %name)



active_term = Terminal

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
    def __init__(self, strd, func_code, termin, bt, line=-1, write=True):
        self.str = strd
        self.bt = bt
        self.w = write
        self.term = termin
        self.relations = {}
        self.fncod = func_code
        self.func_con = func_controller(self.term.func.Get()[func_code] if not callable(func_code) else func_code, bt, self.term)
        self.l = line
        self.term.Objects[strd] = {"rels": self.relations, "fnccon": self.func_con}

    def family(self, ostr, relt):
        try:
            cmd = self.term.Comms[ostr]
            cmd.relations[self.str] = opposite_rels[relt]
            self.term.Objects[ostr]["rels"][self.str] = opposite_rels[relt]
            self.relations[ostr] = relt
            self.term.Objects[self.str]["rels"][ostr] = relt
            if self.w:
                self.term.Delete(self.str, pr=True)
                self.term.Delete(ostr, True)
                self.term.Objects[self.str] = {"rels": self.relations, "fnccon": self.func_con}
                self.term.Comms[self.str] = self
                if not self.bt == "globular" and not callable(self.fncod):
                    self.l = len(self.term.f.load())
                    self.term.f.write("|name:" + self.str, "|fname:" + self.fncod ,self.term.func.GetC()[self.fncod]["code"], "|params:", *self.term.func.GetC()[self.fncod]["params"], "|rels:", *[obj + " " + rel for obj, rel in self.relations.items()], "------------------")
                self.term.Objects[ostr] = {"rels": cmd.relations, "fnccon": cmd.func_con}
                self.term.Comms[ostr] = cmd
                if not cmd.bt == "globular" and not callable(cmd.fncod):
                    cmd.l = len(cmd.term.f.load())
                    cmd.term.f.write("|name:" + cmd.str, "|fname:" + cmd.fncod, cmd.term.func.GetC()[cmd.fncod]["code"],"|params:", *cmd.term.func.GetC()[cmd.fncod]["params"], "|rels:", *[obj + " " + rel for obj, rel in cmd.relations.items()], "------------------")

        except KeyError:
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

def inp(lines: list, pasa, inc):
    global l
    line = input("-"+("-------" if l == 0 else "line:%s"%l if l > 9 else "line:%s-"%l)+"--> ")
    if line.replace(" ", "")[0:2] == "||":
        lc = line.split(" ")
        if lc[0][2:] == "line" and lc[1].isdigit() and int(lc[1]) <= len(lines):
            l = int(lc[1])
        if lc[0][2:] == "code":
            print(''.join(lines))
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
            try:
                NC = compile("def "+name+"("+(', '.join(paras) if paras else "")+"):\n "+''.join(lins[:-2]), name, "exec")
                NF = types.FunctionType(NC.co_consts[0], globals(), name)
                if raises(NF, parastest):
                    print("Error, please try again.")
                    lins = lins[:-2]
                    continue
            except Exception as e:
                print(e)
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
        nonlocal parastest, paras
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
    incorrec = True
    while incorrec:
        while lins[-2:].count(" \n") < 2:
            i = inp(lins, parag, incorrec)
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
                active_term.func.Delete(str(name + "M"), pr=False)
                active_term.Delete(name, pr=False)
                active_term.func.Add(str(name + "M"), ''.join(lins[:-2]), params=paras)
                active_term.Add(name, name + "M")
                active_term.func.AddP(name + "M", parastest)
                incorrec = False

myterm = Terminal("myterm")

myterm.func.Add("geto", "print(objs)", globs={'objs': myterm.Objects})
myterm.func.Add("fam", "if fmt in opposite_rels.keys():\n  objs.Get()[comm].family(fmt, comm1)\n else:\n  print('No such family type')", globs={'opposite_rels': opposite_rels, 'objs': myterm}, params=['comm', 'fmt', 'comm1'])
myterm.func.Add("delt", "term.Delete(nme)", globs={"term": myterm}, params={"nme"})
myterm.func.Add("ex", "sys.exit()", globs={"sys": sys})

myterm.Add("getobjs", 'geto', 'globular')
myterm.Add("create", funcmake)
myterm.Add("edit", funcedit)
myterm.Add("family", 'fam', "globular")
myterm.Add("delete", "delt", "globular")
myterm.Add("stop", "ex", "globular")

command = input("Command: ")

call(myterm, command)