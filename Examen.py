# ------------------------------------------------------------
# calclex.py
#
# tokenizer for a simple expression evaluator for
# numbers and +,-,*,/
# ------------------------------------------------------------

import sys
import ply.lex as lex
import ply.yacc as yacc

#for symbol_table
symbol_table = {}
reserved = 0

# List of token names.   This is always required
tokens = (
     
    'PLUS', 
    'TIMES',
    'EQUALS',
    'TOKEN',
    'NUMBER',
    'CHARACTER',
)

# ----------------- LEXIC ANALYSYS -----------------

# Regular expression rules for simple tokens
t_PLUS = r'\+'
t_TIMES = r'\*'
t_EQUALS = r'='


def t_TOKEN(t):
    r'\d+' #numero
    t.value = int(t.value)    
    return t

def t_NUMBER(t):
    r'\d+' #numero
    t.value = int(t.value)    
    return t

def t_CHARACTER(t):
    r'[a-z]+'    
    return t

t_ignore  = ' \t\n'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# ----------------- SYNTACTIC ANALYSIS -----------------

#raiz del programa
def p_statement(t):
    '''
    statement : operacion empty
        | operacion statement
    '''
    pass

def p_operacion(t):
    '''
    operacion : suma 
        | multiplicacion
    '''

def p_suma(t):
    '''
    suma : TOKEN EQUALS NUMBER PLUS NUMBER
        | TOKEN EQUALS CHARACTER PLUS NUMBER
        | TOKEN EQUALS NUMBER PLUS CHARACTER
        | TOKEN EQUALS CHARACTER PLUS CHARACTER
    '''
# Definicion de los loops
def p_multiplicacion(t):
    '''
    multiplicacion : TOKEN EQUALS NUMBER TIMES NUMBER
        | TOKEN EQUALS CHARACTER TIMES NUMBER
        | TOKEN EQUALS NUMBER TIMES CHARACTER
        | TOKEN EQUALS CHARACTER TIMES CHARACTER
    '''

def p_empty(p):
    'empty : '
    pass


# Manejo de errores de sintaxis 
def p_error(p):
    if p:
        print(f"Error de sintaxis en el token: {p.value}")
    else:
        print("Error de sintaxis al final del archivo")

# -----------------  Build the lexer -----------------
lexer = lex.lex()

data = '''a = 5 + 6'''
           
# Give the lexer some input
lexer.input(data)

# Tokenize
while True:
    tok = lexer.token()
    if not tok: break      # No more input
    print(tok)

parser = yacc.yacc()
parser.parse(data)