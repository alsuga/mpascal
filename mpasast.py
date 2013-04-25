# mpasast.py
# -*- coding: utf-8 -*-
import pydot
'''
Objetos Arbol de Sintaxis Abstracto (AST - Abstract Syntax Tree).

Este archivo define las clases para los diferentes tipos de nodos del
árbol de sintaxis abstracto.  Durante el análisis sintático, se debe 
crear estos nodos y conectarlos.  En general, usted tendrá diferentes
nodos AST para cada tipo de regla gramatical.  Algunos ejemplos de
nodos AST pueden ser encontrados al comienzo del archivo.  Usted deberá
añadir más.
'''

# NO MODIFICAR
class AST(object):
  '''
  Clase base para todos los nodos del AST.  Cada nodo se espera 
  definir el atributo _fields el cual enumera los nombres de los
  atributos almacenados.  El método a continuación __init__() toma
  argumentos posicionales y los asigna a los campos apropiados.
  Cualquier argumento adicional especificado como keywords son 
  también asignados.
  '''
  _fields = []
  def __init__(self,*args,**kwargs):
    assert len(args) == len(self._fields)
    for name,value in zip(self._fields,args):
      setattr(self,name,value)
    # Asigna argumentos adicionales (keywords) si se suministran
    for name,value in kwargs.items():
      setattr(self,name,value)

  def pprint(self):
    for depth, node in flatten(self):
      print("%s%s" % (" "*(4*depth),node))


def validate_fields(**fields):
  def validator(cls):
    old_init = cls.__init__
    def __init__(self, *args, **kwargs):
      old_init(self, *args, **kwargs)
      for field,expected_type in fields.items():
        assert isinstance(getattr(self, field), expected_type)
    cls.__init__ = __init__
    return cls
  return validator

# ----------------------------------------------------------------------
# Nodos AST especificos
#
# Para cada nodo es necesario definir una clase y añadir la especificación
# del apropiado _fields = [] que indique que campos deben ser almacenados.
# A modo de ejemplo, para un operador binario es posible almacenar el
# operador, la expresión izquierda y derecha, como esto:
# 
#    class Binop(AST):
#        _fields = ['op','left','right']
# ----------------------------------------------------------------------

# Unos pocos nodos ejemplos

@validate_fields(function=list)
class Program(AST):
  _fields = ['function']

  def append(self, e):
    self.function.append(e)


@validate_fields(statements=list)
class Statements(AST):
  _fields = ['statements']

  def append(self,e):
    self.statements.append(e)

class Statement(AST):
  _fields = ['statement']

class ConstDeclaration(AST):
  _fields = ['id', 'typename']


@validate_fields(locals=list)
class Locals(AST):
  _fields = ['locals']
  def append(self,e):
    self.locals.append(e)

class Local(AST):
  _fields = ['id', 'typename']

class Local_vec(AST):
  _fields = ['id', 'typename','size']

class Funcdecl(AST):
  _fields = ['id','parameters', 'locals', 'statements']


@validate_fields(parameters=list)
class Parameters(AST):
  _fields = ['parameters']
  def append(self,e):
    self.parameters.append(e)

class Parameters_Declaration(AST):
  _fields = ['id', 'typename']


class Parameters_Declaration_vec(AST):
  _fields = ['id', 'typename','size']

#  def append(self,e):
#    self.append(e)

class Id(AST):
  _fields = ['value']

class Id_vec(AST):
  _fields = ['value','pos']

class Assignment(AST):
  _fields = ['id', 'expression']

class Print(AST):
  _fields = ['liteal']

class Write(AST):
  _fields = ['expression']

class Read(AST):
  _fields = ['id']

class Return(AST):
  _fields = ['expression']
    
class UnaryOp(AST):
  _fields = ['op', 'right']

class BinaryOp(AST):
  _fields = ['op', 'left', 'right']

class Relation(AST):
  _fields = ['op', 'left', 'right']

class Group(AST):
  _fields = ['expression']

class FunCall(AST):
  _fields = ['id', 'parameters']

class IfStatement(AST):
  _fields = ['cond', 'then_b']

class If_elseStatement(AST):
  _fields = ['cond', 'then_b', 'else_b']

class WhileStatement(AST):
  _fields = ['cond', 'body']

class Cast(AST):
  _fields = ['typename','id']

@validate_fields(expressions=list)
class ExprList(AST):
  _fields = ['expressions']  

  def append(self,e):
    self.expressions.append(e)

class Literal(AST):
  '''
  Un valor constante como 2, 2.5, o "dos"
  '''
  _fields = ['value']

class Typename(AST):
  _fields = ['value']


class Empty(AST):
  _fields = []



# Usted deberá añadir mas nodos aquí.  Algunos nodos sugeridos son
# BinaryOperator, UnaryOperator, ConstDeclaration, VarDeclaration, 
# AssignmentStatement, etc...

# ----------------------------------------------------------------------
#                  NO MODIFIQUE NADA AQUI ABAJO
# ----------------------------------------------------------------------

# Las clase siguientes para visitar y reescribir el AST son tomadas
# desde el módulo ast de python .

# NO MODIFIQUE
class NodeVisitor(object):
  '''
  Clase para visitar nodos del árbol de sintaxis.  Se modeló a partir
  de una clase similar en la librería estándar ast.NodeVisitor.  Para
  cada nodo, el método visit(node) llama un método visit_NodeName(node)
  el cual debe ser implementado en la subclase.  El método genérico
  generic_visit() es llamado para todos los nodos donde no hay coincidencia
  con el método visit_NodeName().
  
  Es es un ejemplo de un visitante que examina operadores binarios:

    class VisitOps(NodeVisitor):
      visit_Binop(self,node):
        print("Operador binario", node.op)
        self.visit(node.left)
        self.visit(node.right)
      visit_Unaryop(self,node):
        print("Operador unario", node.op)
        self.visit(node.expr)

    tree = parse(txt)
    VisitOps().visit(tree)
  '''
  def visit(self,node):
    '''
    Ejecuta un método de la forma visit_NodeName(node) donde
    NodeName es el nombre de la clase de un nodo particular.
    '''
    if node:
      method = 'visit_' + node.__class__.__name__
      visitor = getattr(self, method, self.generic_visit)
      return visitor(node)
    else:
      return None
  
  def generic_visit(self,node):
    '''
    Método ejecutado si no se encuentra médodo aplicable visit_.
    Este examina el nodo para ver si tiene _fields, es una lista,
    o puede ser recorrido completamente.
    '''
    for field in getattr(node,"_fields"):
      value = getattr(node,field,None)
      if isinstance(value, list):
        for item in value:
          if isinstance(item,AST):
            self.visit(item)
      elif isinstance(value, AST):
        self.visit(value)

# NO MODIFICAR
class NodeTransformer(NodeVisitor):
  '''
  Clase que permite que los nodos del arbol de sintraxis sean 
  reemplazados/reescritos.  Esto es determinado por el valor retornado
  de varias funciones visit_().  Si el valor retornado es None, un
  nodo es borrado. Si se retorna otro valor, reemplaza el nodo
  original.
  
  El uso principal de esta clase es en el código que deseamos aplicar
  transformaciones al arbol de sintaxis.  Por ejemplo, ciertas optimizaciones
  del compilador o ciertas reescrituras de pasos anteriores a la generación
  de código.
  '''
  def generic_visit(self,node):
    for field in getattr(node,"_fields"):
      value = getattr(node,field,None)
      if isinstance(value,list):
        newvalues = []
        for item in value:
          if isinstance(item,AST):
            newnode = self.visit(item)
            if newnode is not None:
              newvalues.append(newnode)
          else:
            newvalues.append(n)
        value[:] = newvalues
      elif isinstance(value,AST):
        newnode = self.visit(value)
        if newnode is None:
          delattr(node,field)
        else:
          setattr(node,field,newnode)
    return node

# NO MODIFICAR
def flatten(top):
  '''
  Aplana el arbol de sintaxis dentro de una lista para efectos
  de depuración y pruebas.  Este retorna una lista de tuplas de
  la forma (depth, node) donde depth es un entero representando
  la profundidad del arból de sintaxis y node es un node AST
  asociado.
  '''
  class Flattener(NodeVisitor):
    def __init__(self):
      self.depth = 0
      self.nodes = []
    def generic_visit(self,node):
      self.nodes.append((self.depth,node))
      self.depth += 1
      NodeVisitor.generic_visit(self,node)
      self.depth -= 1

  d = Flattener()
  d.visit(top)
  return d.nodes


class DotVisitor():
    graph = None
    num = 1
    def __init__(self):
        self.graph = pydot.Dot("AST", graph_type='digraph')

    def visit(self,node):
        st =""
        if hasattr(node, "value"):
            tmp = getattr(node,"value")
            st+=" => " + str(tmp)
        elif hasattr(node, "op"):
            tmp = getattr(node,"op")
            st+=" => " + str(tmp)
        vertice =pydot.Node("%s " % node.__class__.__name__ + st + " (" + str(self.num)+")" , style="filled", fillcolor="green")
        self.num += 1
        if hasattr(node,"_fields"):
            for field in getattr(node,"_fields"):
                value = getattr(node,field)           
                if isinstance(value,list):
                    for elemento in value:
                        if isinstance(elemento,AST):
                            nvertice = self.visit(elemento)
                            self.graph.add_edge(pydot.Edge(vertice, nvertice))                                         
                elif isinstance(value,AST):
                    nvertice = self.visit(value)
                    self.graph.add_edge(pydot.Edge(vertice, nvertice))
              #else :
               #    nvertice = pydot.Node("%s" % node._fields + " " + str(self.num) , style="filled", fillcolor="green")
               #    self.graph.add_edge(pydot.Edge(vertice, nvertice))
            self.graph.add_node(vertice)
            return vertice          
        

