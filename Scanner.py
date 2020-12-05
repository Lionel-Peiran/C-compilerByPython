
import sys
import re
from collections import namedtuple
from KeyWords import *

Token = namedtuple('Token','type value index')
Word = namedtuple('Word','type RE')
class Scanner:
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
        keyList = keyWords + single_separetor + double_separetor + triple_separetor
        self.REs.append(Word('KEY_WORDS',re.compile('|'.join(keyList))))
        self.REs.append(Word(IDENTIFIER,re.compile(RE_ID)))
        self.REs.append(Word(INTEGER,re.compile(RE_INT)))
        self.REs.append(Word(REAL,re.compile(RE_FLOAT)))
        self.REs.append(Word(STRING,re.compile(RE_STRING)))
        self.REs.append(Word(CHAR,re.compile(RE_CHAR)))
        self.REs.append(Word(SPACE,re.compile(RE_SPACE)))    
    
    def next(self):
        res = Token("ERROR","END_OF_FILE",self.index)
        while self.index < self.sizeofFile:
            res = self.scan()
            if res.type != SPACE:
                if res.type == 'KEY_WORDS':
                    res =Token(res.value,res.value,res.index)
                break
        return res
        
    def scan(self):
        maxIndex = self.index
        res = Token('','','')
        for this in self.REs:
            temp = this.RE.match(self.data,self.index)
            if temp:
                if temp.span()[1] > maxIndex:
                    maxIndex = temp.span()[1]
                    res = Token(this.type,temp.group(),maxIndex)
        self.index = maxIndex
        return res




S = Scanner('demo.c')
while True:
    temp = S.next()
    print(temp)
    if temp.type == "ERROR":
        break
