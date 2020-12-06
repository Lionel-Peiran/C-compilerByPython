from collections import namedtuple
from Scanner import Scanner,Token
from Grammar import PP

INITIAL_STATUS = 0
SHIFT = 'shift'
REDUCE = 'reduce'

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
            action, target = actionTable[self.status[-1]][curToken.type]
            if action == SHIFT:
                self.symbol.append(self.Tokens.__next__())
                self.status.append(target)
            elif action == REDUCE:
                index = target
                left,*right = PP[index]
                lenthBeta = len(right) - 1
                for i in range(lenthBeta):
                    self.symbol.pop()
                    self.status.pop()
                self.symbol.append(left)
                curStatus = self.status[-1]
                self.status.append(gotoTable[curStatus][self.symbol[-1]])
            elif action == SUCCESS:
                self.STATUS = True
                break
            else:
                self.STATUS = False
                break

    
        

P = Parser('demo.c')
