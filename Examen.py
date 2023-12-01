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
    r't[0-9]' #numero 
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

class Node:
    esRaiz = 0
    tipo = ""
    token = ""
    hijoDerecho = ""
    hijoIzquierdo = ""
    def __init__(self,tipo,token,hijoderecho,hijoizquierdo):
         self.tipo = tipo
         self.token = token
         self.hijoDerecho = hijoderecho
         self.hijoIzquierdo = hijoizquierdo
    def setEsRaiz(self, raiz):
        self.esRaiz = raiz
    def getTipo(self):
        return self.tipo
    def getToken(self):
        return self.token
    def getHijoDerecho(self):
        return self.hijoDerecho
    def getHijoIzquierdo(self):
        return self.hijoIzquierdo

ast = []
astMultiplicacion = []
raicesArbolSuma = []
raicesArbolMultiplicacion = []

#raiz del programa
def p_statement(t):
    '''
    statement : operacion
        | operacion statement
    '''

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
        | TOKEN EQUALS NUMBER PLUS TOKEN
        | TOKEN EQUALS TOKEN PLUS NUMBER
        | TOKEN EQUALS TOKEN PLUS CHARACTER
        | TOKEN EQUALS CHARACTER PLUS TOKEN
        | TOKEN EQUALS TOKEN PLUS TOKEN
    '''
    nodo = Node(t[4], t[1],t[3],t[5])
    ast.append(nodo)
    print(t[1], t[2], t[3], t[4],t[5])

# Definicion de los loops
def p_multiplicacion(t):
    '''
    multiplicacion : TOKEN EQUALS NUMBER TIMES NUMBER
        | TOKEN EQUALS CHARACTER TIMES NUMBER
        | TOKEN EQUALS NUMBER TIMES CHARACTER
        | TOKEN EQUALS CHARACTER TIMES CHARACTER
        | TOKEN EQUALS NUMBER TIMES TOKEN
        | TOKEN EQUALS TOKEN TIMES NUMBER
        | TOKEN EQUALS TOKEN TIMES CHARACTER
        | TOKEN EQUALS CHARACTER TIMES TOKEN
        | TOKEN EQUALS TOKEN TIMES TOKEN
    '''
    nodo = Node(t[4], t[1],t[3],t[5])
    ast.append(nodo)
    print(t[1], t[2], t[3], t[4],t[5])

'''def p_empty(p):
    'empty : '
    pass'''

# Manejo de errores de sintaxis 
def p_error(p):
    if p:
        print(f"Error de sintaxis en el token: {p.value}")
    else:
        print("Error de sintaxis al final del archivo")

# -----------------  Build the lexer -----------------
lexer = lex.lex()

data = '''t1 = z + 4 t2 = t1 * c t3 = 3 * t2 t4 = d * t3 t5 = e + f t6 = t5 + g t7 = t6 + h t8 = t1 + t5 t9 = t1 + t7'''
           
# Give the lexer some input
lexer.input(data)

# Tokenize
while True:
    tok = lexer.token()
    if not tok: break      # No more input
    print(tok)

parser = yacc.yacc()
parser.parse(data)

for i in range(len(ast)):
    token = ast[i].getToken()
    repeticiones = 0
    simbolo = ast[i].getTipo()
    for j in range(len(ast)):
        if token == ast[j].getHijoDerecho() or token == ast[j].getHijoIzquierdo():
            repeticiones = repeticiones + 1
            if repeticiones > 1 and simbolo == "+":
                raicesArbolSuma.append(token)
                break
            if repeticiones > 1 and simbolo == "*":
                raicesArbolMultiplicacion.append(token)
                break
    if repeticiones == 0 and simbolo == "+":
        raicesArbolMultiplicacion.append(token)

        
    if repeticiones == 0 and simbolo == "*":
        raicesArbolMultiplicacion.append(token)
                
    token = ""

print("Raices del arbol de sumas")
for i in range(len(raicesArbolSuma)):
    print("Raiz: " + raicesArbolSuma[i])
print("Raices del arbol de multiplicaciones")
for i in range(len(raicesArbolMultiplicacion)):
    print("Raiz: " + raicesArbolMultiplicacion[i])