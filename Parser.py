from collections import namedtuple
from Scanner import Scanner,Token
from Grammar import PP
from Utils import ActionState
from Tools import Load_Table
INITIAL_STATUS = 0
LENGTH_OF_WORD = 26

SHIFT = ActionState.Shift
REDUCE = ActionState.Reduce
SUCCESS = ActionState.Accept

Node = namedtuple('Node','type Children') #tuple，用于生成语法分析书

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
        '''
        暂时使用的语法分析树可视化方法
        '''
        def showLeafNode(leafNode):
            try:
                type,value,index = leafNode
                print(type,'—',value)
            except:
                print(leafNode) 
                return
        def showLevelNode(levelNode,leftSpace):
            n = len(levelNode)
            for i in range(n):
                space = ' ' * (LENGTH_OF_WORD)
                if n == 1:
                    print('—',end='')
                    space += ' '
                elif i == 0:
                    print('┬', end='')
                    space = '│'+(LENGTH_OF_WORD)*' '
                elif i == n-1:
                    print(leftSpace+'└', end='')
                else:
                    space = '│'+(LENGTH_OF_WORD)*' '
                    print(leftSpace+'├', end='')
                
                if isinstance(levelNode[i],Node):
                    print('%s%s' % (levelNode[i].type,'—'*((LENGTH_OF_WORD) - len(levelNode[i].type.encode('gbk')))),end='')
                    showLevelNode(levelNode[i].Children,leftSpace + space)
                else:
                    print('—',end='')
                    showLeafNode(levelNode[i])
        
        for i in self.symbol:
            if isinstance(i,Node):
                print('%s%s' % (i.type,'—'*((LENGTH_OF_WORD) - len(i.type.encode('gbk')))),end='')
                showLevelNode(i.Children,' '*(LENGTH_OF_WORD))
            else:
                showLeafNode(i)
    


