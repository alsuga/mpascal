# mpascheck.py
# -*- coding: utf-8 -*-
'''
Proyecto 3 : Chequeo del Programa
=================================
En este proyecto es necesario realizar comprobaciones semánticas en su programa. 
Hay algunos aspectos diferentes para hacer esto.

En primer lugar, tendrá que definir una tabla de símbolos que haga un seguimiento
de declaraciones de identificadores previamente declarados.  Se consultará la 
tabla de símbolos siempre que el compilador necesite buscar información sobre 
variables y declaración de constantes.

A continuación, tendrá que definir los objetos que representen los diferentes 
tipos de datos incorporados y registrar información acerca de sus capacidades.
Revise el archivo mpastype.py.

Por último, tendrá que escribir código que camine por el AST y haga cumplir un
conjunto de reglas semánticas.  Aquí está una lista completa de todo los que
deberá comprobar:

1.  Nombres y símbolos:

    Todos los identificadores deben ser definidos antes de ser usados.  Esto incluye variables, 
    constantes y nombres de tipo.  Por ejemplo, esta clase de código genera un error:
    
       a = 3;              // Error. 'a' no está definido.
       var a int;

    Note: los nombres de tipo como "int", "float" y "string" son nombres incorporados que
    deben ser definidos al comienzo de un programa (función).
    
2.  Tipos de constantes

    A todos los símbolos constantes se le debe asignar un tipo como "int", "float" o "string".
    Por ejemplo:

       const a = 42;         // Tipo "int"
       const b = 4.2;        // Tipo "float"
       const c = "forty";    // Tipo "string"

    Para hacer esta asignación, revise el tipo de Python del valor constante y adjunte el
    nombre de tipo apropiado.

3.  Chequeo de tipo operación binaria.

    Operaciones binarias solamente operan sobre operandos del mismo tipo y produce un
    resultado del mismo tipo.  De lo contrario, se tiene un error de tipo.  Por ejemplo:

    var a int = 2;
    var b float = 3.14;

    var c int = a + 3;    // OK
    var d int = a + b;    // Error.  int + float
    var e int = b + 4.5;  // Error.  int = float

4.  Chequeo de tipo operador unario.

    Operadores unarios retornan un resultado que es del mismo tipo del operando.

5.  Operadores soportados

    Estos son los operadores soportados por cada tipo:

    int:      binario { +, -, *, /}, unario { +, -}
    float:    binario { +, -, *, /}, unario { +, -}
    string:   binario { + }, unario { }

    Los intentos de usar operadores no soportados debería dar lugar a un error.
    Por ejemplo:

    var string a = "Hello" + "World";     // OK
    var string b = "Hello" * "World";     // Error (op no soportado *)

6.  Asignación.

    Los lados izquierdo y derecho de una operación de asignación deben ser 
    declarados del mismo tipo.

    Los valores sólo se pueden asignar a las declaraciones de variables, no
    a constantes.

Para recorrer el AST, use la clase NodeVisitor definida en mpasast.py.
Un caparazón de código se proporciona a continuación.
'''

import sys, re, string, types
from errors import error
from mpasast import *
import mpastype
import mpaslex

class SymbolTable(object):
 
  def __init__(self, parent=None):
    self.entries = {}
    self.parent = parent

#  def lookup(self, a):
#    return self.entries.get(a)

  def add(self, name, value):
    if self.entries.has_key(name):
      if not self.entries[name].extern:
        raise Symtab.SymbolDefinedError()
      elif self.entries[name].type.get_string() != \
        value.type.get_string():
        raise Symtab.SymbolConflictError()
    self.entries[name] = value

  def lookup(self, name):
    if self.entries.has_key(name):
      return self.entries[name]
    else:
      if self.parent != None:
        return self.parent.lookup(name)
      else:
        return None


class CheckProgramVisitor(NodeVisitor):
  def __init__(self):
    # Inicializa la tabla de simbolos
    self.symtab = SymbolTable()
    self.func = {}

    # Agrega nombre de tipos incorporados ((int, float, string) a la tabla de simbolos
    self.symtab.add("int",mpastype.int_type)
    self.symtab.add("float",mpastype.float_type)
    self.symtab.add("string",mpastype.string_type)
    self.symtab.add("bool",mpastype.boolean_type)
    self.symtab.add("void",mpastype.void_type)

  def visit_Program(self,node):
    # 1. Visita todas las declaraciones (statements)
    # 2. Registra la tabla de simbolos asociada
    for i in node.function:
      self.visit(i)

  def visit_IfStatement(self, node):
    self.visit(node.cond)
    if node.cond.type != mpastype.boolean_type:
      error(node.lineno, "Tipo incorrecto para condicion if")
    else:
      self.visit(node.then_b)
      if node.else_b:
        self.visit(node.else_b)

  def visit_WhileStatement(self, node):
    self.visit(node.cond)
    if not node.cond.type == mpastype.boolean_type:
      error(node.lineno, "Tipo incorrecto para condicion while")
    else:
      self.visit(node.body)

  def visit_UnaryOp(self, node):
    self.visit(node.right)
    if not node.right.type == None:
      if not mpaslex.operators[node.op] in node.right.type.un_ops:
        error(node.lineno, "Operacion no soportada con este tipo")
    else:
      error(node.lineno, "Operacion invalida")
    node.type = node.right.type

  def visit_BinaryOp(self, node):
    self.visit(node.left)
    self.visit(node.right)
    if node.left.type != node.right.type:
      error(node.lineno, "No coinciden los tipos de los operandos en la operacion con '%s'" % node.op)
    if node.left.type == None or node.right.type == None:
      error(node.lineno, "Los operadores no tienen un tipo")
      node.type = self.symtab.lookup("void")
    else:
      if node.op == "+" or node.op == "-" or node.op == "*" or node.op == "/":
        node.type = node.left.type
      else:
        node.type = self.symtab.lookup("bool")

  def visit_Assignment(self,node):
    self.visit(node.location)
    sym = self.symtab.lookup(node.location.id)
    if sym == None:
      error(node.lineno,"El id '%s' no ha sido definido" % node.location.id)
    self.visit(node.expression)
    if(sym != node.expression.type):
      error(node.lineno,"No coinciden los tipos en la asignacion '%s'" % node.location.id)
   
  # def visit_ConstDeclaration(self,node):
  #   # 1. Revise que el nombre de la constante no se ha definido
  #   if self.symtab.lookup(node.id):
  #     error(node.lineno, "Simbolo '%s' ya definido" % node.id)
  #   # 2. Agrege una entrada a la tabla de símbolos
  #   else:
  #     self.symtab.add(node.id, node)
  #   self.visit(node.value)
  #   node.type = node.value.type

  def visit_Local(self,node):
    if self.symtab.lookup(node.id):
      error(node.lineno, "Identificador '%s' ya definido" % node.id)
    else:
      self.symtab.add(node.id, self.looktype(node.typename))
    if getattr(node,"size") != None :
      self.visit(getattr(node,"size"))
      if node.size.type != self.symtab.lookup("int"):
        error(node.lineno,"Tamaño del vector mal definido")
    node.type = self.symtab.lookup(node.typename)

  def visit_Location(self,node):
    if node.pos:
      self.visit(node.pos)
      if node.pos.type != self.symtab.lookup("int") : 
        error(node.lineno, "Acceso invalido al vector")
    if self.symtab.entries.has_key(node.id):
      node.type = self.symtab.lookup(node.id)
    else:
      error(node.lineno, "El id '%s' no ha sido definido" % node.id)
      node.type = self.symtab.lookup("void")

  def visit_Literal(self,node):
    # Adjunte un tipo apropiado a la constante
    if isinstance(node.value, types.BooleanType):
      node.type = self.symtab.lookup("bool")
    elif isinstance(node.value, types.IntType):
      node.type = self.symtab.lookup("int")
    elif isinstance(node.value, types.FloatType):
      node.type = self.symtab.lookup("float")
    elif isinstance(node.value, types.StringTypes):
      node.type = self.symtab.lookup("string")

  def visit_Funcdecl(self, node):
    if self.symtab.lookup(node.id):
      error(node.lineno, "El identificador de la funcion '%s' ya esta definido" % node.id)
      pass
    self.symtab.add(node.id, self.symtab.lookup("void"))
    self.push_symtab()
    for i in node.parameters.parameters:
      if i == None: break
      self.visit(i)
      self.addfunc(node.id,i.type)
    self.visit(node.locals)
    self.visit(node.statements)
    if self.symtab.entries.has_key("return"):
      node.type = self.symtab.lookup("return") 
    else:
      node.type = self.symtab.lookup("void")
    self.pop_symtab()
    self.symtab.entries[node.id] = node.type

  def visit_FunCall(self, node):
    if self.symtab.lookup(node.id) == None:
      error(node.lineno, "Funcion '%s' no definida" % node.id)
    if self.func.has_key(node.id):
      for i,j in zip(node.parameters.expressions, self.func[node.id]):
        self.visit(i)
        if(i.type != j):
          error(node.lineno, "Tipo erroneo de argumentos en el llamado a la funcion '%s'" % node.id)   
    else:
      pass
    node.type = self.symtab.lookup(node.id)

  def visit_Parameters_Declaration(self, node):
    if(self.symtab.lookup(node.id) != None ):
      error(node.lineno,"Variable '%s' ya definida" % node.id)
    else:
      node.type = self.symtab.lookup(node.typename)
      self.symtab.add(node.id,node.type)

  def visit_Group(self, node):
    self.visit(node.expression)
    node.type = node.expression.type

  def visit_Relation(self, node):
    self.visit(node.left)
    self.visit(node.right)
    if node.left.type != node.right.type:
      error(node.lineno, "Operandos de relación no son del mismo tipo")
    elif not mpaslex.operators[node.op] in node.left.type.bin_ops:
      error(node.lineno, "Operación no soportada con este tipo")
    node.type = self.symtab.lookup('bool')

  def visit_Return(self, node):
    self.visit(node.expression)
    if not self.symtab.entries.has_key("return"):
      self.symtab.add("return", node.expression.type)
    elif(self.symtab.lookup("return") != node.expression.type):
      error(node.lineno,"La funcion retorna dos tipos de dato distintos")

  def visit_Cast(self,node):
    self.visit(node.expression)
    if node.typename == "int" or node.typename=="float":
      node.type = self.symtab.lookup(node.typename)
    else:
      error(node.lineno,"Cast invalido")
      node.type = self.symtab.lookup("void")

  def visit_Empty(self, node):
    pass

  def addfunc(self,key,value):
    if self.func.has_key(key):
      self.func[key].append(value)
    else:
      self.func[key] = [value]

  def looktype(self,at):
    at_type = at + "_type"
    realtype = getattr(mpastype,at_type)
    return realtype

  def push_symtab(self):
    self.symtab = SymbolTable(self.symtab)

  def pop_symtab(self):
    self.symtab = self.symtab.parent

  def generic_visit(self,node):
    if getattr(node,"_fields") : 
      for field in getattr(node,"_fields"):
        value = getattr(node,field,None)
        if isinstance(value, list):
          for item in value:
            if isinstance(item,AST):
              self.visit(item)
        elif isinstance(value, AST):
          self.visit(value)
    else :
      pass



# ----------------------------------------------------------------------
#                       NO MODIFICAR NADA DE LO DE ABAJO
# ----------------------------------------------------------------------

def check_program(node):
  '''
  Comprueba el programa suministrado (en forma de un AST)
  '''
  checker = CheckProgramVisitor()
  checker.visit(node)

def main():
  import mpasparse
  import sys
  from errors import subscribe_errors
  lexer = mpaslex.make_lexer()
  parser = mpasparse.make_parser()
  with subscribe_errors(lambda msg: sys.stdout.write(msg+"\n")):
    program = parser.parse(open(sys.argv[1]).read())
    # Revisa el programa
    check_program(program)

if __name__ == '__main__':
  main()
