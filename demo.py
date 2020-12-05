from Grammar import keyWords
import re

a = '|'.join(keyWords)
with open('demo.c') as f:
    data = f.read()
    
    print(data)    