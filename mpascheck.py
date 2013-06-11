# mpascheck.py
# -*- coding: utf-8 -*-

import sys, re, string, types
from errors import error
from mpasast import *
import mpastype
import mpaslex

class SymbolTable(object):
 
  def __init__(self, parent=None):
    self.entries = {}
    self.parent = parent
    self.func = {}

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

  def lookfun(self, name):
    if self.func.has_key(name):
      return self.func[name]
    else:
      if self.parent != None:
        return self.parent.lookfun(name)
      else:
        return None

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
    self.in_c = 0
    self.actfun = ""
    self.vecs = {}
    self.ret = False

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
    self.in_c += 1
    if not node.cond.type == mpastype.boolean_type:
      error(node.lineno, "Tipo incorrecto para condicion while")
    else:
      self.visit(node.body)
    self.in_c -= 1

  def visit_UnaryOp(self, node):
    self.visit(node.right)
    if not node.right.type == None:
      if not mpaslex.operators[node.op] in node.right.type.un_ops:
        error(node.lineno, "Operacion no soportada con este tipo")
    elif hasattr(node.right,"pos") :
      if not node.right.pos:
        error(node.lineno, "No se pueden hacer este tipo de operacion con vectores")
    else:
      error(node.lineno, "Operacion invalida")
    node.type = node.right.type

  def visit_BinaryOp(self, node):
    self.visit(node.left)
    self.visit(node.right)
    if node.left.__class__.__name__ == "Location":
      if self.vecs[self.actfun].has_key(node.left.id):
        if node.left.pos == None and self.vecs[self.actfun][node.left.id]  >0: 
          error(node.lineno, "No se pueden hacer este tipo de operacion con vectores")
    if node.right.__class__.__name__ == "Location":
      if self.vecs[self.actfun].has_key(node.right.id):
        if node.right.pos == None and self.vecs[self.actfun][node.right.id]  > 0:
          error(node.lineno, "No se pueden hacer este tipo de operacion con vectores")
    if node.left.type == self.symtab.lookup("void") or node.right.type == self.symtab.lookup("void"):
      node.type = self.symtab.lookup("void")
    elif node.left.type != node.right.type:
      error(node.lineno, "No coinciden los tipos de los operandos en la operacion con '%s'" % node.op)
    elif node.left.type == None or node.right.type == None:
      error(node.lineno, "Los operadores no tienen un tipo")
      node.type = self.symtab.lookup("void")
    else:
      if node.op == "+" or node.op == "-" or node.op == "*" or node.op == "/":
        node.type = node.left.type
      else:
        node.type = self.symtab.lookup("bool")

  def visit_Assignment(self,node):
    self.visit(node.location)
    if self.vecs[self.actfun].has_key(node.location.id):
      if self.vecs[self.actfun][node.location.id] != 0 and not node.location.pos:
          error(node.lineno, "No se puede asignar la expresion al vector %s" % node.location.id) 
    sym = self.symtab.lookup(node.location.id)
    if sym == None:
      error(node.lineno,"El id '%s' no ha sido definido" % node.location.id)
    self.visit(node.expression)
    if(sym != node.expression.type):
      error(node.lineno,"No coinciden los tipos en la asignacion '%s'" % node.location.id)
    if(hasattr(node.expression,"pos")):
      if not node.expression.pos and self.vecs[self.actfun][node.expression.id] > 0:
        error(node.lineno, "Asignacion no permitida")
   
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
    self.vecs[self.actfun][node.id] = 0
    if getattr(node,"size"):
      self.visit(getattr(node,"size"))
      if node.size.type != self.symtab.lookup("int"):
        error(node.lineno,"Tamaño del vector mal definido")
      self.vecs[self.actfun][node.id] = node.size.value           
    node.type = self.symtab.lookup(node.typename)

  def visit_Location(self,node):
    if self.vecs[self.actfun].has_key(node.id):
      if node.pos and self.vecs[self.actfun][node.id] == 0:
          error(node.lineno, "El identificador '%s' no es un vector" % node.id)
      if node.pos:
        self.visit(node.pos)
        if node.pos.type != self.symtab.lookup("int") : 
          error(node.lineno, "Acceso invalido al vector")
      if self.symtab.lookup(node.id):
        node.type = self.symtab.lookup(node.id)
    else:
      error(node.lineno, "El identificador '%s' no ha sido definido" % node.id)
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
    tm = False
    if self.symtab.lookup(node.id):
      error(node.lineno, "El identificador de la funcion '%s' ya esta definido" % node.id)
      return
    self.symtab.add(node.id, self.symtab.lookup("void"))
    self.push_symtab()
    self.vecs[node.id] = {}
    tmp = self.actfun
    self.actfun = node.id
    for i in node.parameters.parameters:
      if i == None: break
      self.visit(i)
      self.addfunc(node.id,i)
    self.visit(node.locals)
    tm = self.check_return(node.statements)
    if self.symtab.entries.has_key("return"):
      node.type = self.symtab.lookup("return")
    else:
      node.type = self.symtab.lookup("void")
    self.visit(node.statements)
    self.pop_symtab()
    self.symtab.entries[node.id] = node.type
    self.actfun = tmp
    if self.ret:
      error(node.lineno, "No se puede identificar el tipo de dato de retorno")
    if not tm and self.symtab.lookup(node.id).name != "void":
      error(node.lineno, "No se retorna en todas las sentencias de desicion")
    self.ret = False

  def visit_FunCall(self, node):    
    if not self.symtab.lookfun(node.id):
      error(node.lineno, "Funcion '%s' no definida" % node.id)
    if self.symtab.lookup(node.id) == self.symtab.lookup("void") : 
      node.type = self.symtab.lookup("void")
      pass
    if self.symtab.lookfun(node.id):
      if(len(node.parameters.expressions) == len(self.symtab.lookfun(node.id))):
        for i,j in zip(node.parameters.expressions, self.symtab.lookfun(node.id)):
          self.visit(i)
          if hasattr(i,"pos"):
            if (self.vecs[self.actfun][i.id] > 0 and not getattr(i,"pos") and not getattr(j,"size"))or \
            (self.vecs[self.actfun][i.id] == 0 and getattr(j,"size")) or \
            (self.vecs[self.actfun][i.id] !=  self.vecs[node.id][j.id]):
              error(node.lineno, "Tamaño de la variable incompatible en el llamado a la funcion '%s'" % node.id)
          elif self.vecs[node.id][j.id] != 0 and getattr(j,"size"):
              error(node.lineno, "Se espera un vector en el llamado a la funcion '%s'" % node.id)
          if i.type != j.type :
            error(node.lineno, "Tipo erroneo de argumentos en el llamado a la funcion '%s'" % node.id)
      else :
        error(node.lineno, "Numero erroneo de argumentos en el llamado a la funcion '%s'" % node.id)
    else:
      pass
    node.type = self.symtab.lookup(node.id)


  def visit_Parameters_Declaration(self, node):
    if(self.symtab.entries.has_key(node.id)):
      error(node.lineno,"Variable '%s' ya definida" % node.id)
    else:
      node.type = self.symtab.lookup(node.typename)
      self.symtab.add(node.id,node.type)
      if getattr(node,"size"):
        self.vecs[self.actfun][node.id] = node.size.value
      else:
        self.vecs[self.actfun][node.id] = 0

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
    self.ret = False
    if (not self.symtab.entries.has_key("return")) or self.symtab.lookup("return")  == self.symtab.lookup("void"):
      if(node.expression.type.name == "void"):
        self.ret = True
      self.symtab.entries["return"] =  node.expression.type
    elif(self.symtab.lookup("return") != node.expression.type and node.expression.type != self.symtab.lookup("void")):
      error(node.lineno,"La funcion retorna dos tipos de dato distintos")

  def visit_Cast(self,node):
    self.visit(node.expression)
    if node.typename == "int" or node.typename=="float":
      node.type = self.symtab.lookup(node.typename)
    else:
      error(node.lineno,"Cast invalido")
      node.type = self.symtab.lookup("void")

  def visit_Break(self,node):
    if self.in_c == 0:
      error(node.lineno, "Break fuerda de un ciclo")

  def visit_Read(self,node):
    self.visit(node.location)
    if self.vecs[self.actfun][node.location.id] > 0 and not getattr(node.location,"pos"):
      error(node.lineno, "No se puede leer a un vector")

  def visit_Write(self,node):
    self.visit(node.expression)
    if node.expression.type == self.symtab.lookup("void"):
        error(node.lineno, "No se puede escribir esta expresion")
    if hasattr(node.expression,"pos"):
      if not self.vecs[self.actfun].has_key(node.expression.id):
        pass
      elif self.vecs[self.actfun][node.expression.id] > 0 and not getattr(node.expression,"pos"):
        error(node.lineno, "No se puede escribir un vector")


  def visit_Empty(self, node):
    pass

  def check_return(self, node):
    if hasattr(node,"statements"):
      tmp = False
      ret = False
      ifs = False
      for i in node.statements:
        if i.__class__.__name__ == "Return" :
          self.visit_Return(i)
          ret = True
        elif hasattr(i,"body"): 
          tmp = self.check_return(i.body)
        elif hasattr(i,"then_b") : 
          ifs = self.check_return(i.then_b)
          if getattr(i,"else_b") :
            temporal = self.check_return(i.else_b)
            ifs = (not ifs and temporal) or (ifs and not temporal)
      if ret:
        return True
      elif tmp or ifs:
        return False
      else :
        return True
    elif node.__class__.__name__ == "Return" :
      self.visit_Return(node)
    return True

  def addfunc(self,key,value):
    if self.symtab.parent.func.has_key(key):
      self.symtab.parent.func[key].append(value)
    else:
      self.symtab.parent.func[key] = [value]

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
