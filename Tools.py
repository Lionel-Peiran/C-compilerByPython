from collections import defaultdict, namedtuple, OrderedDict
from functools import reduce
import pickle

from Utils import *
from Grammar import PP, Book

Item = namedtuple('Item', 'pid dot ahead')

'''
    Input:
        Grammar_Table   产生式
    
    Output:
        NullS           NULLABLE集
        可以直接推出空串的集合

    Func:
        求解Nullable集
'''
def Nullable_Set(Grammar_Table):
    NullS = set()
    while True:
        Flag = False
        for lhs, *rhs in Grammar_Table:
            if lhs in NullS:
                continue
            #   A -> ε  |   A -> BC...,  B,C,... in NullS
            if (len(rhs) == 1 and rhs[-1] == Empty_Symbol) or all(map(lambda i: i in NullS, rhs)):
                NullS.add(lhs)
                Flag = True
        if not Flag:
            break
    return NullS

'''
    Input:
        Grammar_Table   产生式
    
    Output:
        TerminalS       终结符
        即不能单独出现在推导式左边的符号，也就是说终结符不能再进行推导。
    
    Func:
        求解Terminal集
'''
def Terminal_Set(Grammar_Table):
    TerminalS = set()
    NotTerminalS = set()
    for lhs, *rhs in Grammar_Table:
        NotTerminalS.add(lhs)
        TerminalS = reduce(lambda S, term: S | set([term]), rhs, TerminalS)

    TerminalS = TerminalS - NotTerminalS
    return TerminalS

'''
    Input:
        terms           式子右边的项
        FirstS          First集
        TerminalS       Terminal集

    
    Output:
        TerminalS       终结符

    Func:
        求解单独一个式子的First集
'''
def First_Closure(terms, FirstS, TerminalS, NullS):
    curClosure = set()
    for term in terms:
        if term in TerminalS:
            curClosure.add(term)
            return curClosure
        else:
            curClosure = curClosure.union(FirstS[term])
            if term not in NullS:
                return curClosure
    return curClosure


'''
    Input:
        Grammar_Table   产生式
        TerminalS       Terminal集
        NullS           Nullable集
    
    Output:
        FirstS          First集

    Func:
        求解整个产生式的First集
'''
def First_Set(Grammar_Table, Terminal, NullS):
    First = defaultdict(set)
    while True:
        OriginFirst = First.copy()
        for lhs, *rhs in Grammar_Table:
            First[lhs] = First[lhs] | First_Closure(rhs, First, Terminal, NullS)
        if OriginFirst == First:
            break
    return First


'''
    Input:
        Grammar_Table   产生式
        FirstS          First集
        TerminalS       Terminal集
        NullS           Nullable集
    
    Output:
        FollowS         Follow集

    Func:
        求解整个产生式的Follow集
'''
def Follow_Set(Grammar_Table, FirstS, Terminal, NullS):
    Follow = defaultdict(set)

    while True:
        Flag = False
        for lhs, *rhs in Grammar_Table:
            cur = Follow[lhs]
            for term in rhs[::-1]:
                if term in Terminal:
                    cur = Follow[term]
                else:
                    if cur - Follow[term]:
                        Follow[term] = cur.union(Follow[term])
                        Flag = True
                    if term in NullS:
                        cur = cur.union(FirstS[term])
                    else:
                        cur = FirstS[term]
        if not Flag:
            break

    return Follow


'''
    Input:
        terms           式子右边的项
        NullS           Nullable集
   
    Output:
        Null            Nullable集

    Func:
        求解单独一个式子的Nullable集
'''
def Nullable_Closure(terms, NullS):
    return all(map(lambda i: i in NullS, terms))


'''
    Input:
        terms           式子右边的项
        Extended_Table  增广产生式
        FirstS          First集
        TerminalS       Terminal集
        NullS           Nullable集
    
    Output:
        Closure         求该项的闭包

    Func:
        求出一个项集的闭包
'''
def Calc_Closure(items, Extended_Table, FirstS, TerminalS, NullS):
    LookUp = defaultdict(list)
    for id, (lhs, *rhs) in enumerate(Extended_Table):
        LookUp[lhs].append(id)

    curClosure = set(items)

    while True:
        Flag = False
        for s in curClosure.copy():
            lhs, *rhs = Extended_Table[s.pid]
            # 对于每一个形如 A -> a*Bb, c 的项
            if len(rhs) > s.dot and rhs[s.dot] not in TerminalS:
                fs = First_Closure(rhs[s.dot+1:], FirstS, TerminalS, NullS)
                if Nullable_Closure(rhs[s.dot+1:], NullS): 
                    fs = fs.union(s.ahead)
                for pid in LookUp[rhs[s.dot]]:
                    term = Item(pid, 0, tuple(fs))
                    if term not in curClosure:
                        curClosure.add(term)
                        Flag = True
        if not Flag:
            break

    return curClosure


def Goto(items, X, Extended_Table, FirstS, TerminalS, NullS):
    res = set()
    for item in items:
        pos = Extended_Table[item.pid]
        if (item.dot+1) < len(pos) and pos[item.dot+1] == X:
            clo = Calc_Closure({Item(item.pid, item.dot+1, item.ahead)}, Extended_Table, FirstS, TerminalS, NullS)
            res = res.union(clo)
    return res


def LR1_Table(Extended_Table, FirstS, TerminalS, NullS, Start_Symbol):

    Extended_Table = Extended_Table[:]
    Extended_Table.insert(0, ('S', Start_Symbol))
    for i in range(len(Extended_Table)):
        if Extended_Table[i][-1] == 'ε' and len(Extended_Table[i]) == 2:
            Extended_Table[i] = (Extended_Table[i][0],)
    TerminalS = TerminalS.copy()
    TerminalS.add('$')


    Action_Table = defaultdict(dict)
    Goto_Table = defaultdict(dict)
    
    c = Calc_Closure({Item(0, 0, ('$',))}, Extended_Table, FirstS, TerminalS, NullS)
    State = [c] 
    Queue = [0] 
    while Queue:
        cid = Queue.pop()
        print(len(Queue))
        for item in State[cid]:
            lhs, *rhs = Extended_Table[item.pid]
            if len(rhs) == item.dot:
                for ahead in item.ahead:
                    Action_Table[cid][ahead] = (ActionState.Reduce, item.pid)  
                    if item.pid == 0:
                        Action_Table[cid][ahead] = (ActionState.Accept, item.pid)
            elif rhs[item.dot] not in Action_Table[cid] and (rhs[item.dot] not in Goto_Table[cid]): 
                c = Goto(State[cid], rhs[item.dot],
                         Extended_Table, FirstS, TerminalS, NullS)
                try:
                    index = State.index(c)
                except ValueError:
                    State.append(c)
                    index = len(State) - 1
                    Queue.append(index)
                if rhs[item.dot] in TerminalS:
                    Action_Table[cid][rhs[item.dot]] = (ActionState.Shift, index) 
                else:
                    Goto_Table[cid][rhs[item.dot]] =  index
                    
    return Extended_Table, Action_Table, Goto_Table


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

    Extended_Table, Action_Table, Goto_Table = LR1_Table(S, FIRST, TERMINAL, Nullable, Start_Symbol='translation_unit')
    pickle.dump((Extended_Table, dict(Action_Table), dict(Goto_Table)), open('parse_table.dat', 'wb'))
