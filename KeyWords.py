keyWords = ['union', 'char', 'static', 'struct', 'extern', 'signed', 'goto', 'do', 'default',
            'short', 'double', 'enum', 'unsigned', 'const', 'float',
            'auto', 'continue', 'void', 'sizeof', 'else', 'volatile', 'register', 'int',
            'return', 'break', 'if', 'typedef', 'for', 'switch', 'while', 'case', 'long','main']

single_separetor = ['\[', '&', '>', '-', '=', '\}', '\)', '%', '\*', '\^',
                    '\+', '\{', '!', ';', '<', '\]', '\(', '\:', '/', '\?', '\.', ',', '\|', '~']

double_separetor = ['!=', '--', '&=', '\*=', '^=', '\|\|', '\+=', '>>', '->',
                    '\+\+', '&&', '<<', '/=', '-=', '\|=', '==', '%=', '>=', '<=']

triple_separetor = ['<<=', '>>=']

IDENTIFIER = 'id'
RE_ID = '[a-zA-Z_][a-zA-Z_0-9]*'

INTEGER = 'int_const'
RE_INT = '\d+'

FLOAT = 'float_const'
RE_FLOAT = '-?\d+\.\d+?'

STRING = 'string'
RE_STRING = '\".+?\"'

CHAR = 'char_const'
RE_CHAR = '\'.{1}\''

SPACE = 'NULL'
RE_SPACE = '\s+'

RE_REMARK0 = '//.*?\n' #解决//格式的注释
RE_REMARK1 = '/\*[^*]*\*+([^/*][^*]*\*+)*/' #解决/**/格式的多行注释

ERR_ID = "ERROR_ID"
RE_ERR_ID = '[\d]+[a-zA-Z_][a-zA-Z_0-9]*'