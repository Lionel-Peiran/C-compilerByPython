
import sys
import re
from collections import namedtuple
from KeyWords import *

Token = namedtuple('Token','type value index')
class Scanner:
    def __init__(self,filePath):
        self.data = ''
        with open(filePath) as f:
            self.data = f.read()
        keyList = keyWords + single_separetor + double_separetor + triple_separetor
        self.KeyWordPattern = re.compile('|'.join(keyList))
        

    
    def next(self):
        pass

    def scan(self):
        print(self.rePattern.match(self.data,4).group())


S = Scanner('demo.c')
S.scan()

