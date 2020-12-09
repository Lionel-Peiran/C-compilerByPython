
import sys
import re
from collections import namedtuple
from KeyWords import *

Token = namedtuple('Token','type value index')
Word = namedtuple('Word','type RE')
class Scanner:
    '''
    类构造函数，输入需要被分析文件的路径
    '''
    def __init__(self,filePath):
        self.data = ''
        self.REs = []
        self.index = 0
        self.sizeofFile = 0
        with open(filePath) as f:
            self.data = f.read()
        # 解决注释
        self.data,_ = re.subn(RE_REMARK0,'\n',self.data)
        self.data,_ = re.subn(RE_REMARK1,'',self.data)
        self.sizeofFile = len(self.data)
        # 准备匹配
        keyList = keyWords + triple_separetor + double_separetor + single_separetor  
        self.REs.append(Word('KEY_WORDS',re.compile('|'.join(keyList))))
        self.REs.append(Word(IDENTIFIER,re.compile(RE_ID)))
        self.REs.append(Word(INTEGER,re.compile(RE_INT)))
        self.REs.append(Word(FLOAT,re.compile(RE_FLOAT)))
        self.REs.append(Word(STRING,re.compile(RE_STRING)))
        self.REs.append(Word(CHAR,re.compile(RE_CHAR)))
        self.REs.append(Word(SPACE,re.compile(RE_SPACE)))
        self.REs.append(Word(ERR_ID,re.compile(RE_ERR_ID)))    
    '''
    调用此方法可生成一个迭代器，用于返回下个词的Token
    此方法调用scan函数，处理其返回的Token并返回
    '''
    def next(self):
        while self.index < self.sizeofFile:
            res = self.scan()
            if res.type != SPACE:
                if res.type == 'KEY_WORDS':
                    yield Token("'%s'" % res.value,res.value,res.index)
                elif res.type == ERR_ID:
                    yield Token("ERROR","ID_INVALID",res.index)
                else:
                    yield res
        yield Token("$","$",self.index)
        
    '''
    私有函数，使用正则表达式进行匹配，返回当前匹配到的一个词的Token
    '''  
    def scan(self):
        maxIndex = self.index
        res = Token('','','')
        for this in self.REs:
            temp = this.RE.match(self.data,self.index)
            if temp:
                if temp.span()[1] > maxIndex:
                    maxIndex = temp.span()[1]
                    res = Token(this.type,temp.group(),maxIndex)
        if self.index != maxIndex:
            self.index = maxIndex
        else:
            return Token('ERROR','UNABLE_TO_MATCH',self.index)
        return res
