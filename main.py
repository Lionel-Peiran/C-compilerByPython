from Tools import Load_Table
from Parser import Parser

if __name__ == "__main__":
    Extended_Table, Action_Table, Goto_Table = Load_Table()
    P = Parser('test.c')
    P.parser(Extended_Table,Action_Table,Goto_Table)
    P.showParserTree()