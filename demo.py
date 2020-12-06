import re
from collections import namedtuple
from Grammar import PP

Token = namedtuple('Token','type value index')
a = Token(2,2,2)
print(a[0])
