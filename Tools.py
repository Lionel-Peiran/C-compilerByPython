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
    #if len(ps) == 1 and ps[-1] == 'ε':
    #    return set()
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
            #if len(rhs) == 1 and rhs[-1] == 'ε':
            #    continue
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

def NullableSet(productions):
    """
    计算Nullable集
    """
    p = productions
    nulls = set()
    changing = True
    while changing:
        changing = False
        for left, *right in p:
            if left in nulls:
                continue
            if len(right) == 1 and right[-1] == 'ε':
                nulls.add(left)
                changing = True
            elif all(map(lambda i: i in nulls, right)):  # 右部全为nullable
                nulls.add(left)
                changing = True

    return nulls


def First(productions, terminal, nullable):
    p = productions
    first = defaultdict(set)
    changing = True
    while changing:
        changing = False
        origin = first.copy()
        for left, *right in p:
            
            res = First_S(right, first, terminal, nullable)
            if res:
                changing = True
            first[left] = first[left] | res

        if origin == first:
            break
    return first


def First_S(ps, first, terminal, nullable, left=None, follow=None):
    """
    计算串的First集合， 如果传入了left（左部），则为计算left->ps推导式的select集
    """
    if len(ps) == 1 and ps[-1] == 'ε':
        return set()
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



def Follow(productions, fitst, terminal, nullable):
    """
    计算Follow集
    """
    p = productions
    follow = defaultdict(set)
    changing = True
    while changing:
        changing = False
        for left, *right in p:
            if len(right) == 1 and right[-1] == 'ε':
                continue
            temp = follow[left]
            for b in right[::-1]:
                if b in terminal:
                    temp = follow[b]
                else:
                    if temp-follow[b]:
                        follow[b] = temp.union(follow[b])
                        changing = True
                    if b in nullable:
                        temp = temp.union(fitst[b])
                    else:
                        temp = fitst[b]

    return follow

def goto(items, X, productions, FIRST, TERMINAL, Nullable):

    res = set()
    for item in items:
        p = productions[item.pid]
        if (item.dot+1) < len(p) and p[item.dot+1] == X:
            c = Calc_Closure({Item(item.pid, item.dot+1, item.ahead)},
                        productions, FIRST, TERMINAL, Nullable)
            res = res.union(c)
    return res


def LR1_parse_table(Grammar_Table, FIRST, TERMINAL, Nullable, start_symbol='<程序>'):

    Extended_Table = Grammar_Table.copy()
    Extended_Table.insert(0, ('S', start_symbol))
    for i in range(len(Extended_Table)):
        if Extended_Table[i][-1] == 'ε' and len(Extended_Table[i]) == 2:
            Extended_Table[i] = (Extended_Table[i][0],)
    TERMINAL = TERMINAL.copy()
    TERMINAL.add('$')

    Action_Table = defaultdict(dict)
    Goto_Table = defaultdict(dict)

    c = Calc_Closure({Item(0, 0, ('$',))}, Extended_Table, FIRST, TERMINAL, Nullable)
    
    states = [c]
    StateQueue = [0]
    
    while StateQueue:
        curState = StateQueue.pop()

        #print(len(StateQueue))
            
        for item in states[curState]:
            lhs, *rhs = Extended_Table[item.pid]

            #   It's time to Reduce & Accept !
            if len(rhs) == item.dot:
                for ahead in item.ahead:
                    if item.pid == 0:
                        Action_Table[curState][ahead] = (ActionState.Accept, item.pid)
                    else:
                        Action_Table[curState][ahead] = (ActionState.Reduce, item.pid)

            elif rhs[item.dot] not in Action_Table[curState]:
                c = goto(states[curState], rhs[item.dot],
                         Extended_Table, FIRST, TERMINAL, Nullable)
                try:
                    nextState = states.index(c)
                except ValueError:
                    states.append(c)
                    nextState = len(states)-1
                    StateQueue.append(nextState)
                
                if rhs[item.dot] in TERMINAL:
                    Action_Table[curState][rhs[item.dot]] = (ActionState.Shift, nextState) 
                else:
                    Goto_Table[curState][rhs[item.dot]] = nextState

    return Extended_Table, Action_Table, Goto_Table
def Load_Table():
    fp = open('parse_table.dat', 'rb') 
    #Extended_Table, Action_Table, Goto_Table, = pickle.load(fp)
    Extended_Table, Action_Table, Goto_Table = pickle.load(fp)
    return Extended_Table, Action_Table, Goto_Table
if __name__ == '__main__':
    
    Extended_Table, Action_Table, Goto_Table = Load_Table()
    for i in range(len(Action_Table)):
        print(i, " : ", Action_Table[i])
    
    print(Goto_Table)

    '''
    S = Book
    
    TERMINAL = Terminal_Set(S)
    #print(TERMINAL)
    Nullable = NullableSet(S)
    #print(Nullable)
    FIRST = First(S, TERMINAL, Nullable)
    #print(FIRST)
    #print(First_Set(S, TERMINAL, Nullable))
    FOLLOW = Follow(S,FIRST, TERMINAL, Nullable)
    #print(FOLLOW)

    print("Begin Table Trans")
    Extended_Table, Action_Table, Goto_Table = LR1_parse_table(S, FIRST, TERMINAL, Nullable, start_symbol='Goal')

    pickle.dump((Extended_Table, dict(Action_Table),  dict(Goto_Table)), open('parse_table.dat', 'wb'))

    for i in range(len(Action_Table)):
        print(i, " : ", Action_Table[i])
    
    print(Goto_Table)
    #for i in range(len(Goto_Table)):
    #    print(i, " : ", Goto_Table[i])

    Extended_Table, Action_Table, Goto_Table = Load_Table()
    print(Action_Table)
    print(Goto_Table)

    '''