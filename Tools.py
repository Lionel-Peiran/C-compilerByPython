from collections import defaultdict, namedtuple, OrderedDict
from functools import reduce
import pickle

from Utils import *
from Grammar import PP, Book

Item = namedtuple('Item', 'pid dot ahead')


def Nullable_Set(Grammar_Table):
    NullS = set()
    while True:
        Flag = False
        for lhs, *rhs in Grammar_Table:
            if lhs in NullS:
                continue
            if (len(rhs) == 1 and rhs[-1] == Empty_Symbol) or all(map(lambda i: i in NullS, rhs)):
                NullS.add(lhs)
                Flag = True
        if not Flag:
            break
    return NullS

def Terminal_Set(Grammar_Table):
    TerminalS = set()
    NotTerminalS = set()
    for lhs, *rhs in Grammar_Table:
        NotTerminalS.add(lhs)
        TerminalS = reduce(lambda S, term: S | set([term]), rhs, TerminalS)

    TerminalS = TerminalS - NotTerminalS
    return TerminalS

def First_Closure(ps, first, terminal, nullable, left=None, follow=None):
    res = set()
    for b in ps:
        if b in terminal:
            res.add(b)
            return res
        else:
            res = res.union(first[b])
            if b not in nullable:
                return res
    if left and follow:
        res.add(follow[left])
    return res

def First_Set(Grammar_Table, Terminal, NullS):
    First = defaultdict(set)
    while True:
        OriginFirst = First.copy()
        for lhs, *rhs in Grammar_Table:
            First[lhs] = First[lhs] | First_Closure(rhs, First, Terminal, NullS)
        if OriginFirst == First:
            break
    return First

def Follow_Set(Grammar_Table, FirstS, Terminal, NullS):
    Follow = defaultdict(set)
    changing = True
    while changing:
        changing = False
        for lhs, *rhs in Grammar_Table:
            cur = Follow[lhs]
            for term in rhs[::-1]:
                if term in Terminal:
                    cur = Follow[term]
                else:
                    if cur - Follow[term]:
                        Follow[term] = cur.union(Follow[term])
                        changing = True
                    if term in NullS:
                        cur = cur.union(FirstS[term])
                    else:
                        cur = FirstS[term]

    return Follow

def Nullable_Closure(ps, nullable):
    return all(map(lambda i: i in nullable, ps))

def Calc_Closure(iniClosure, Grammar_Table, FirstS, TerminalS, NullS):
    LookUp = defaultdict(list)
    for id, (lhs, *rhs) in enumerate(Grammar_Table):
        LookUp[lhs].append(id)

    curClosure = set(iniClosure)

    changing = True
    while changing:
        changing = False

        for term in curClosure.copy():
            lhs, *rhs = Grammar_Table[term.pid]

            if len(rhs) > term.dot and rhs[term.dot] not in TerminalS:

                curSel = First_Closure(rhs[term.dot+1:], FirstS, TerminalS, NullS)

                if Nullable_Closure(rhs[term.dot+1:], NullS):
                    curSel = curSel.union(term.ahead)

                for pid in LookUp[rhs[term.dot]]:
                    term = Item(pid, 0, tuple(curSel))
                    if term not in curClosure:
                        curClosure.add(term)
                        changing = True

    return curClosure

def closure(items, productions, FIRST, TERMINAL, Nullable):
    LookUp = defaultdict(list)
    for id, (lhs, *right) in enumerate(productions):
        LookUp[lhs].append(id)

    res = set(items)
    changing = True
    while changing:
        changing = False
        for s in res.copy():
            lhs, *right = productions[s.pid]
            # 对于每一个形如 A -> a*Bb, c 的项
            if len(right) > s.dot and right[s.dot] not in TERMINAL: # 项可展开
                fs = First_Closure(right[s.dot+1:], FIRST, TERMINAL, Nullable)
                if Nullable_Closure(right[s.dot+1:], Nullable):  # Bc可为空
                    fs = fs.union(s.ahead)
                for pid in LookUp[right[s.dot]]:
                    t = Item(pid, 0, tuple(fs))
                    if t not in res:
                        res.add(t)
                        changing = True

    return res


def goto(items, X, productions, FIRST, TERMINAL, Nullable):
    res = set()
    for item in items:
        p = productions[item.pid]
        if (item.dot+1) < len(p) and p[item.dot+1] == X:
            c = closure({Item(item.pid, item.dot+1, item.ahead)}, productions, FIRST, TERMINAL, Nullable)
            res = res.union(c)
    return res


def LR1_parse_tableOld(productions, FIRST, TERMINAL, Nullable, start_symbol='<程序>'):

    productions = productions[:]
    productions.insert(0, ('S', start_symbol))  # 增广文法
    for i in range(len(productions)):
        if productions[i][-1] == 'ε' and len(productions[i]) == 2:
            productions[i] = (productions[i][0],)
    TERMINAL = TERMINAL.copy()
    TERMINAL.add('$')


    Action_Table = defaultdict(dict)
    Goto_Table = defaultdict(dict)
    
    #Action_Table = defaultdict(dict)
    c = closure({Item(0, 0, ('$',))}, productions, FIRST, TERMINAL, Nullable)
    states = [c]  # closure
    unresolve = [0]  # closure id that need resolve
    while unresolve:
        cid = unresolve.pop()
        print(len(unresolve))
        for item in states[cid]:
            left, *right = productions[item.pid]
            if len(right) == item.dot:  # 规约项
                for ahead in item.ahead:
                    Action_Table[cid][ahead] = (ActionState.Reduce, item.pid)  # 设置action为”规约“
                    if item.pid == 0:
                        Action_Table[cid][ahead] = (ActionState.Accept, item.pid)  # 设置action为”接受“
            elif right[item.dot] not in Action_Table[cid] and (right[item.dot] not in Goto_Table[cid]):  # 未处理的移进项目和待归约项目
                c = goto(states[cid], right[item.dot],
                         productions, FIRST, TERMINAL, Nullable)
                try:
                    index = states.index(c)
                except ValueError:
                    states.append(c)
                    index = len(states)-1
                    unresolve.append(index)
                if right[item.dot] in TERMINAL:
                    Action_Table[cid][right[item.dot]] = (ActionState.Shift, index)  # 设置action为”移进“
                else:
                    Goto_Table[cid][right[item.dot]] =  index
    return productions, Action_Table, Goto_Table


def Load_Table():
    fp = open('parse_table.dat', 'rb') 
    #Extended_Table, Action_Table, Goto_Table, = pickle.load(fp)
    Extended_Table, Action_Table, Goto_Table = pickle.load(fp)
    return Extended_Table, Action_Table, Goto_Table

def Old_table():
    fp = open('parse_table.dat', 'rb') 
    productions,parse_tab = pickle.load(fp)
    return parse_tab,productions

if __name__ == '__main__':
    
    S = PP
    TERMINAL = Terminal_Set(S)
    Nullable = Nullable_Set(S)
    FIRST = First_Set(S, TERMINAL, Nullable)
    FOLLOW =  Follow_Set(S,FIRST, TERMINAL, Nullable)

    Extended_Table, Action_Table, Goto_Table = LR1_parse_tableOld(S, FIRST, TERMINAL, Nullable, start_symbol='translation_unit')
    pickle.dump((Extended_Table, dict(Action_Table), dict(Goto_Table)), open('parse_table.dat', 'wb'))
