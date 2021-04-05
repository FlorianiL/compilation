import ply.lex as lex

tokens = (
    'DUMBO_OPEN',
    'DUMBO_CLOSE',
    'AFFECT',
    'VAR',
    'STRING',
    'END_LINE',
    'PAR_OPEN',
    'PAR_CLOSE',
    'SEPARATOR'

)

t_ignore = ' |\t'

t_DUMBO_OPEN = r'{{'
t_DUMBO_CLOSE = r'}}'
t_AFFECT = r':='
t_VAR = r'[a-zA-Z_]\w*'
t_STRING = r'\'[\w\s](\w|\s)*\''
t_END_LINE = r';'
t_PAR_OPEN = r'\('
t_PAR_CLOSE = r'\)'
t_SEPARATOR = r','


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print("Illegalcharacter '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()


def run_lex(data):
    lexer.input(data)
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)
