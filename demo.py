import re
from collections import namedtuple

string = '1223acsdfa'
RE = '^[\d]+[a-zA-Z_][a-zA-Z_0-9]*'
RE = re.compile(RE)
print(RE.match(string))