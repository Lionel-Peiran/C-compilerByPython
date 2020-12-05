import re
from collections import namedtuple

SPACE = re.compile('ccs')
string = 'cc'

print(SPACE.match(string))