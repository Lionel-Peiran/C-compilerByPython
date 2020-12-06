from collections import namedtuple
from Scanner import Scanner,Token
from Grammar import PP
from Utils import ActionState
from Tools import Load_Table
INITIAL_STATUS = 0
SHIFT = ActionState.Shift
REDUCE = ActionState.Reduce
SUCCESS = ActionState.Accept

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
            
            action, target = actionTable[self.status[-1]][curToken.type]
            print(actionTable[self.status[-1]][curToken.type])
            
            input()

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
                new_status = Goto_Table[self.status[-1]][left]
                self.status.append(new_status)
                self.symbol.append(Node(left,reduct_body))
            elif action == SUCCESS:
                self.STATUS = True
                print('SUCCESSFUL')
                break
            else:
                self.STATUS = False
                break
        '''
        states = [0]  # 状态栈
        symbols = []  # 符号栈

        
        self.Tokens.append(Token('$', None, 30))
        curr_token_index = 0
        while True:
            
            token = self.Tokens[curr_token_index]
            terminal = token[0]
            action, action_data = trans_tab[states[-1]][terminal]
            print("cur_token:")
            print(token)

            print(action)
            print(action_data)
            print(states)
            print(symbols)
            input()
            if action == 0:  # 移进
                symbols.append(token)
                states.append(action_data)
                curr_token_index += 1
            # print('移进', terminal)
            elif action == 1:  # 规约
                left, *right = productions[action_data]
                reduct_body = symbols[-len(right):] if right else [Token('ε', None, None)]
                for _ in range(len(right)):
                    states.pop()
                    symbols.pop()
                _, new_state = trans_tab[states[-1]][left]
                states.append(new_state)
                symbols.append(Node(left, reduct_body))
            elif action == 2:  # 接受
                break
        '''
Extended_Table, Action_Table, Goto_Table = Load_Table()
P = Parser('demo.c')


P.parser(Extended_Table,Action_Table,Goto_Table)
