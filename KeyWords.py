keyWords = ['union', 'char', 'static', 'struct', 'extern', 'signed', 'goto', 'do', 'default',
            'short', 'double', 'enum', 'unsigned', 'const', 'float',
            'auto', 'continue', 'void', 'sizeof', 'else', 'volatile', 'register', 'int',
            'return', 'break', 'if', 'typedef', 'for', 'switch', 'while', 'case', 'long','main']

single_separetor = ['\[', '&', '>', '-', '=', '\}', '\)', '%', '\*', '\^',
                    '\+', '\{', '!', ';', '<', '\]', '\(', '\:', '/', '\?', '\.', ',', '\|', '~']

double_separetor = ['!=', '--', '&=', '\*=', '^=', '\|\|', '\+=', '>>', '->',
                    '\+\+', '&&', '<<', '/=', '-=', '\|=', '==', '%=', '>=', '<=']

triple_separetor = ['<<=', '>>=']

IDENTIFIER = {type:'id',RE:r''}
INTEGER = 'int_const'
BOOL = 'int_const'
REAL = 'float_const'
STRING = 'string'

