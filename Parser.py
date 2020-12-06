from collections import namedtuple
from Scanner import Scanner,Token
from Grammar import PP
from Utils import ActionState
from Tools import Load_Table,Old_table
INITIAL_STATUS = 0
LENGTH_OF_WORD = 18

SHIFT = ActionState.Shift
REDUCE = ActionState.Reduce
SUCCESS = ActionState.Accept
'''
SHIFT = 0
REDUCE = 1
SUCCESS = 2
'''
Node = namedtuple('Node','type Children')

class Parser(object):
    """
    docstring
    """
    def __init__(self,path:str):
        self.S = Scanner(path)
        self.Tokens = list(self.S.next())
        self.status = []
        self.symbol = []
        self.STATUS = False
    def parser(self,extendTable,actionTable,gotoTable):
        # print(self.Tokens)
        cur_Token_index = 0
        self.Tokens.append(Token('$','$',self.S.sizeofFile))
        self.status.append(INITIAL_STATUS)
        while True:
            curToken = self.Tokens[cur_Token_index]
            print(curToken)
            print(self.status)
            action, target = actionTable[self.status[-1]][curToken.type]
            print(actionTable[self.status[-1]][curToken.type])
            
            # input()

            if action == SHIFT: 
                self.symbol.append(curToken)
                self.status.append(target)
                cur_Token_index += 1
            elif action == REDUCE:
                index = target
                left,*right = extendTable[index]
                lenthBeta = len(right)
                reduct_body = self.symbol[-len(right):]
                for i in range(lenthBeta):
                    self.symbol.pop()
                    self.status.pop()
                # _,new_status = gotoTable[self.status[-1]][left]
                new_status = gotoTable[self.status[-1]][left]
                self.status.append(new_status)
                self.symbol.append(Node(left,reduct_body)) # 用符号栈保存语法分析树
            elif action == SUCCESS:
                self.STATUS = True
                print('SUCCESSFUL')
                break
            else:
                self.STATUS = False
                break
    def showParserTree(self):
        def showLeafNode(leafNode):
            try:
                type,value,index = leafNode
                print(type,'—',value)
            except:
                print(leafNode) 
                return
        def showLevelNode(levelNode,leftSpace):
            for i in range(len(levelNode)):
                pass
        for i in self.symbol:
            if isinstance(i,Node):
                print('%s%s' % n.NT,'—'*((LENGTH_OF_WORD - 2) - len(i.type)),end='')
                showLevelNode(i.Children,' '*(LENGTH_OF_WORD - 1))
            else:
                showLeafNode(i)
    

Extended_Table, Action_Table, Goto_Table = Load_Table()
# Action_Table, Extended_Table = Old_table()
P = Parser('demo.c')
P.parser(Extended_Table,Action_Table,Goto_Table)
