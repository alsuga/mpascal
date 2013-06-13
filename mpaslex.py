#!/usr/bin/env python
# mpaslex.py

from errors import error

from ply.lex import lex


tokens = [
  # keywords
  'ID', 'PRINT', 'FUNC', 'RETURN',
  'BEGIN', 'THEN', 'END','READ','WRITE',

  # Control flow
  'IF', 'ELSE', 'WHILE', 'BREAK', 'SKIP','DO',

  # Operators and delimiters
  'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
  'ASSIGN', 'SEMI', 'LPAREN', 'RPAREN', 'COMMA',
  'COLON','LBRACKET','RBRACKET',

  # Boolean operators
  'LT', 'LE', 'GT', 'GE', 'LAND', 'LOR', 'LNOT',
  'EQ', 'NE',

  # Literals
  'INTEGER', 'FLOAT', 'STRING', 
  
  # Datatype
  'TYPENAME',
]

t_ignore = ' \t\r'

t_PLUS      = r'\+'
t_MINUS     = r'-'
t_TIMES     = r'\*'
t_DIVIDE    = r'/'
t_ASSIGN    = r':='
t_SEMI      = r';'
t_LPAREN    = r'\('
t_RPAREN    = r'\)'
t_COMMA     = r','
t_LBRACKET  = r'\['
t_RBRACKET  = r'\]'
t_LT        = r'<'
t_LE        = r'<='
t_EQ        = r'=='
t_GE        = r'>='
t_GT        = r'>'
t_NE        = r'!='
t_LAND      = r'and'
t_LOR       = r'or'
t_LNOT      = r'not'
t_COLON     = r':'

def t_TYPENAME(t):
  r'\b(int|bool|float)\b'
  return t
# ----------------------------------------------------------------------
# *** DEBE COMPLETAR : escriba las regexps y codigo adicional para ***
#
# Tokens para literales, INTEGER, FLOAT, STRING. 

# Constantes punto flotante.   Deben ser reconocidos numeros de punto
# flotante en formatos como se muestra en los ejemplos siguientes:
#
#   1.23, 1.23e1, 1.23e+1, 1.23e-1, 123., .123, 1e1, 0.
#
# El valor debe ser convertido a un float de Python cuando se analice
def t_FLOAT(t):
  r'(?:(?:\d*\.\d+|\d+\.\d*)(?:[eE][-+]?\d+)?)|(?:\d+[eE][-+]?\d+)'
  t.value = float(t.value)               # Conversion a float de Python
  return t

# Constantes enteras.  Se debe reconocer enteros en todos los formatos
# siguientes:
#
#     1234             (decimal)
#     01234            (octal)
#     0x1234 or 0X1234 (hex)
#
# El valor debe ser convertido a un int de Python cuando se analice.
def t_INTEGER(t):
  r'(?:0[xX]?)?\d+'
  # Conversion a int de Python
  if t.value.startswith(('0x','0X')):
    t.value = int(t.value,16)              
  elif t.value.startswith('0'):
    t.value = int(t.value,8)
  else:
    t.value = int(t.value)
  return t

# Constantes string.  Se debe reconocer texto entre comillas.
# Por ejemplo:
#
#     "Hola Mundo"
#
# A las cadenas se les permite tener codigos de escape los cuales
# estan definidos por un backslash inicial.   Los siguientes 
# codigos backslash deben ser reconocidos:
#      
#       \n    = newline (10)
#       \r    = carriage return (13) 
#       \t    = tab (9)
#       \\    = char baskslash (\)
#       \"    = comilla (")
#       \bhh  = codigo caracter byte hh  (h es un digito hex)
#
# Todas los otros codigos de escape deberan dar un error. Nota: las 
# literales de string *NO* comprenden el rango completo de codigos de
# caracter soportados por Python.
#
# El valor del token debe ser la cadena con todos los codigo de escape
# reemplazados por su correspondiente codigo de caracter raw.

escapes_not_b = r'nrt\"'
escapes = escapes_not_b + "b"

def _replace_escape_codes(t):
  newval = []
  ostring = iter(t.value)
  olen = len(t.value)
  Nerr = False
  for c in ostring:
    if c=='"':
      error(t.lexer.lineno,"Fin de cadena prematuro")
      Nerr = True
      break
    elif c=='\\':
      c1 = ostring.next()
      #if c1 not in escapes_not_b:

      if c1 not in escapes :
        error(t.lexer.lineno,"Codigo secuencia escape mala '%s'" % (c+c1))
        Nerr = True
        break
      else:
        if c1=='n':
          c='\\n'
        elif c1=='r':
          c='\\r'
        elif c1=='t':
          c='\\t'
        elif c1=='\\':
          c='\\\\'
        elif c1=='"':
          c='"'
        elif c1=="b":
        	b = ostring.next()+ostring.next()
        	if (str.isdigit(b[0]) or (str.lower(b[0]) >= 'a' and str.lower(b[0]) <= 'f')) and (str.isdigit(b[1]) or (str.lower(b[1]) >= 'a' and str.lower(b[1]) <= 'f')):
        		c1 = '\\b'
        		c = c1+b
        	else:
        		error(t.lexer.lineno,"Codigo secuencia escape mala '%s'" % (c+c1))
        		Nerr = True
        		break
    newval.append(c)
  
  t.value = ''.join(newval)

  if Nerr :
  	t.lexer.skip(len(t.value))
  else:
  	return t

def t_STRING(t):
  r'".*?"'
  # Convierta t.value a una cadena con codigo de escape reemplazado por valor actual.
  t.value = t.value[1:-1]
  _replace_escape_codes(t)    # Debe implementar arriba
  return t


#def t_BOOLEAN(t):
#  r'\b(true|false)\b'
#  t.value = True if t.value=='true' else False
#  return t

# ----------------------------------------------------------------------
# *** DEBE COMPLETAR: Escrina la regexp y agrege la palabra ***
#

# Identificadores y palabras reservadas.
# Coincidir un identificador raw.  Los identificadores siguen las mismas
# reglas de Python. Esto es, ellos comienzan con una letra o subrayado (_)
# y puede contener un numero arbitrario de letras, digitos o subrayado 
# despues de este.
def t_ID(t):
  r'[a-zA-Z_]\w*'
  t.type = reserved.get(t.value,'ID')
  return t

# *** DEBE IMPLEMENTAR ***
# Adicione codigo para coincidir con palabras reservadas como 'var', 'const',
# 'print', 'func', 'extern'

reserved = {
  'if':'IF',
  'else':'ELSE',
  'while':'WHILE',
  'func':'FUNC',
  'fun':'FUNC',
  'print':'PRINT',
  'begin':'BEGIN',
  'end':'END',
  'then':'THEN',
  'break' : 'BREAK',
  'read' : 'READ',
  'write' : 'WRITE',
  'return' : 'RETURN',
  'skip' : 'SKIP',
  'do' : 'DO',
  'and' : 'LAND',
  'or' : 'LOR',
  'not' : 'LNOT',
}

operators = {
  r'+' : "PLUS",
  r'-' : "MINUS",
  r'*' : "TIMES",
  r'/' : "DIVIDE",
  r':=' : "ASSIGN",
  r';' : "SEMI",
  r'(' : "LPAREN",
  r')' : "RPAREN",
  r',' : "COMMA",
  r':' : "COLON",
  r'<' : "LT",
  r'<=' : "LE",
  r'==' : "EQ",
  r'>=' : "GE",
  r'>' : "GT",
  r'!=' : "NE",
  r'and' : 'LAND',
  r'or' : 'LOR',
  r'not' : 'LNOT',
}

# ----------------------------------------------------------------------
# *** DEBE COMPLETAR : Escriba las regexps adecuadas ***
#
# Ignore texto.  Las siguientes reglas debeb ser usadas para ignorar
# texto en el archivo de entrada.  Esto incluye comentarios y lineas
# en blanco.

# Una o mas lineas en blanco
def t_newline(t):
  r'\n+'
  t.lexer.lineno += len(t.value)

# Comentarios C-style (/* ... */)
def t_COMMENT(t):
  r'/\*(.|\n)*?\*/'
  t.lexer.lineno += t.value.count('\n')

# Comentarios C++-style (//...)
def t_CPPCOMMENT(t):
  r'//.*?\n'
  t.lexer.lineno += 1

# Comentario pascal
def t_PASCOMMENT(t):
  r'{(.|\n)*?}'
  t.lexer.lineno += t.value.count('\n')

# ----------------------------------------------------------------------
# *** DEBE COMPLETAR : Agrege las regexps indicadas ***
#
# Manejo de error.  Las condiciones siguientes de error deben ser 
# manejadas por su analizador lexico.

# Caracteres ilegales (manejo errores generico)
def t_error(t):
  error(t.lexer.lineno,"Caracter ilegal %r" % t.value[0])
  t.lexer.skip(1)

# Comentario C-style no terminado
def t_COMMENT_UNTERM(t):
  r'(?:/\*[.\n]*(?!\*/))|(?:{[.\n]*(?!}))'
  error(t.lexer.lineno, "Comentario no terminado")
  exit(0)


# Literal de cadena no terminada
def t_STRING_UNTERM(t):
  r'".*(?!")'
  error(t.lexer.lineno,"Literal de cadena no terminada")
  t.lexer.lineno += 1
  t.lexer.skip(1)

#def t_ILEGAL(t):
#	r'(?:.*\*/)|(?:.*})'
#	error(t.lexer.lineno,"Expresion ilegal")
#	t.lexer.skip(len(t.value))

# ----------------------------------------------------------------------
#                NO CAMBIE NADA DEBAJO DE ESTA PARTE
# ----------------------------------------------------------------------
def make_lexer():
  '''
  Funcion de utilidad para crear el objeto lexer
  '''
  return lex()

if __name__ == '__main__':
  import sys
  from errors import subscribe_errors

  if len(sys.argv) != 2:
    sys.stderr.write("Usage: %s filename\n" % sys.argv[0])
    raise SystemExit(1)

  lexer = make_lexer()
  with subscribe_errors(lambda msg: sys.stderr.write(msg+"\n")):
    lexer.input(open(sys.argv[1]).read())
    for tok in iter(lexer.token,None):
      sys.stdout.write("%s\n" % tok)
