from Tools import Load_Table
from Parser import Parser
import sys
if __name__ == "__main__":
    try:Extended_Table, Action_Table, Goto_Table = Load_Table()
    except:
        print("分析表未找到，请先阅读Usage，运行python Tools.py生成分析表")
        exit(-1)
    try : P = Parser(sys.argv[1])
    except:
        print("请先阅读Usage，按正确方法使用")
        print("Example command : python main.py demo.c")
        exit(-1)
    if(P.parser(Extended_Table,Action_Table,Goto_Table)):
        P.showParserTree()