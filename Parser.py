from collections import namedtuple
from Scanner import Scanner,Token
from Grammar import PP
from Utils import ActionState
from Tools import Load_Table
INITIAL_STATUS = 0
SHIFT = ActionState.Shift
REDUCE = ActionState.Reduce

Node = namedtuple('Node','type Children')

class Parser(object):
    """
    docstring
    """
    def __init__(self,path:str):
        self.S = Scanner(path)
        self.Tokens = self.S.next()
        self.status = []
        self.symbol = []
        self.STATUS = False
    def parser(self,actionTable,gotoTable):
        self.status.append(INITIAL_STATUS)
        self.symbol.append(Token('$','$',self.S.sizeofFile))
        while True:
            curToken = self.Tokens.__next__()
            print(curToken.type)
            print(actionTable[self.status[-1]])
            print(self.status[-1])
            action, target = actionTable[self.status[-1]][curToken.type
            print(target)
            input()

            if action == SHIFT: 
                self.symbol.append(self.Tokens.__next__())
                self.status.append(target)
            elif action == REDUCE:
                index = target
                left,*right = PP[index]
                lenthBeta = len(right)
                children = []
                for i in range(lenthBeta):
                    children.append(self.symbol.pop())
                    self.status.pop()
                self.symbol.append(Node(left,children))
                curStatus = self.status[-1]
                self.status.append(gotoTable[curStatus][self.symbol[-1].type])
            elif action == SUCCESS:
                self.STATUS = True
                print('SUCCESSFUL')
                break
            else:
                self.STATUS = False
                break

Extended_Table, Action_Table, Goto_Table = Load_Table()
P = Parser('demo.c')

P.parser(Action_Table,Goto_Table)
