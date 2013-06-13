# mpascode.py
# -*- coding: utf-8 -*-
'''
Proyecto 4 - Parte 1
====================
Generación de código para MiniPascal.  En este proyecto, se va a convertir 
el AST dentro de un código de máquina intermedio conocido como Asignación
Estática Única (SSA - Single Static Assignment).  Hay alguna partes 
importantes que se necesitan saber para hacer este trabajo.  Por favor, 
lea cuidadosamente antes de iniciar:

Single Static Assignment
========================
El primer problema es como descomponer expresiones complejas en algo que
se pueda manejar mas sencillamente.  Una forma de hacer esto es descomponer
todas las expresiones dentro de una secuencia de asignaciones sencillas 
invocando operaciones binarias o unarias.

Como un ejemplo, supóngase que se tiene una expresión matemática como esta:

    2 + 3*4 - 5

Esta es una manera posible de descomponer la expresion dentro de operaciones
sencillas:

    int_1 = 2
    int_2 = 3
    int_3 = 4
    int_4 = int_2 * int_3
    int_5 = int_1 + int_4
    int_6 = 5
    int_7 = int_5 - int_6

En este código, las variables int_n son simplemente temporales usadas durante
la realización de los cálculos.  Una característica crítica de SSA es que 
tales variables temporales sólo se asignan una vez (asignación única) y nunca
se vuelve a utilizar.  Por lo tanto, si se tuviera que evaluar otra expresión,
solo tendría que incrementar los números.  Por ejemplo, si se fuera a evaluar
10+20+30, se tendría un código como este:

    int_8 = 10
    int_9 = 20
    int_10 = int_8 + int_9
    int_11 = 30
    int_12 = int_11 + int_11

SSA está destinado a imitar las instrucciones de bajo nivel que se podrían 
llevar a cabo en una CPU.  Por ejemplo, las instrucciones anteriores pueden
ser traducidas a instrucciones de máquina de bajo nivel (para una CPU
hipotética) de esta manera:

    MOVI   #2, R1
    MOVI   #3, R2
    MOVI   #4, R3
    MUL    R2, R3, R4
    ADD    R4, R1, R5
    MOVI   #5, R6
    SUB    R5, R6, R7

Otro de los beneficios de SSA es que es muy fácil de codificar y manipular
usando estructuras de datos sencillas tales como tuplas.  Por ejemplo, se
puede codificar la secuencia de operaciones anterior como una lista como esta:

     [ 
     ('movi', 2, 'int_1'),
     ('movi', 3, 'int_2'),
     ('movi', 4, 'int_3'),
     ('mul', 'int_2', 'int_3', 'int_4'),
     ('add', 'int_1', 'int_4', 'int_5'),
     ('movi', 5, 'int_6'),
     ('sub', 'int_5','int_6','int_7'),
     ]

Tratando con Variables
======================
En su programa, probablemente se tendrá algunas variables que reciben y se 
asignan diferentes valores.  Por ejemplo:

     a = 10 + 20;
     b = 2 * a;
     a = a + 1;

En "puro SSA", todas las variables en realidad serán versionadas como
temporales en las expresiones anteriores.  Por ejemplo, se emitirá código
como este:

     int_1 = 10
     int_2 = 20
     a_1 = int_1 + int_2
     int_3 = 2
     b_1 = int_3 * a_1
     int_4 = 1 
     a_2 = a_1 + int_4
     ...

Por rezones que tienen sentido despues, vamos a tratar a las variables 
declaradas como localizaciones de memoria y acceder a ellas usando
instrucciones load/store.  Por ejemplo:

     int_1 = 10
     int_2 = 20
     int_3 = int_1 + int_2
     store(int_3, "a")
     int_4 = 2
     int_5 = load("a")
     int_6 = int_4 * int_5
     store(int_6,"b")
     int_7 = load("a")
     int_8 = 1
     int_9 = int_7 + int_8
     store(int_9, "a")

Una palabra sobre tipos
=======================
En bajo nivel, la CPU puede solamente operar con muy pocos tipos
diferentes de datos como ints y floats.  Debido a la semántica de
los tipos de bajo-nivel podrían variar ligeramente, se tendrá que
tomar algunas medidas para manejarlos separadamente.

En nuestro código intermedio, estamos llendo simplemente a los nombres
de etiquetas de las variables temporables e instrucciones con un tipo
asociado de bajo nivel.  Por ejemplo:

    2 + 3*4          (ints)
    2.0 + 3.0*4.0    (floats)

El código intermedio generado podría lucir como este:

    ('literal_int', 2, 'int_1')
    ('literal_int', 3, 'int_2')
    ('literal_int', 4, 'int_3')
    ('mul_int', 'int_2', 'int_3', 'int_4')
    ('add_int', 'int_1', 'int_4', 'int_5')

    ('literal_float', 2.0, 'float_1')
    ('literal_float', 3.0, 'float_2')
    ('literal_float', 4.0, 'float_3')
    ('mul_float', 'float_2', 'float_3', 'float_4')
    ('add_float', 'float_1', 'float_4', 'float_5')

Nota: Estos tipos pueden o no corresponder directamente a los nombres de
los tipos usados en el programa de entrada.  Por ejemplo, durante la
traducción, estructuras de datos de mas alto nivel deben se reducidas a
operaciones de bajo nivel.

Su tarea
========
Su tarea es la siguiente: Escriba una clase Visitor() AST que tome un 
programa en MiniPascal y lo aplane a una única secuencia de instrucciones 
de código de SSA representadas como tuplas de la forma

     (operacion, operandos, ..., destinacion)
     
Para empezar, su código SSA deberá solamente contener las siguientes 
operaciones:

     ('alloc_type',varname)             # Localizar una variable de un tipo dado
     ('literal_type', value, target)    # Carga un valor constante dentro de target
     ('load_type', varname, target)     # Carga el valor de una variable dentro de target
     ('store_type',source, varname)     # Almacena el valor de source dentro de varname
     ('add_type', left, right, target ) # target = left + right
     ('sub_type',left,right,target)     # target = left - right
     ('mul_type',left,right,target)     # target = left * right
     ('div_type',left,right,target)     # target = left / right  (truncamiento entero)
     ('uadd_type',source,target)        # target = +source
     ('uneg_type',source,target)        # target = -source
     ('print_type',source)              # Imprime el valor de source
'''

import mpasast
import mpasblock
from mpasblock import BasicBlock, IfBlock, WhileBlock
from collections import defaultdict

# PASO 1: Mapeo de los simbolos de operadores tales como +, -, *, / 
# a nombres de opcode actual como 'add', 'sub', 'mul', 'div' para 
# ser emitidos como código SSA.  Esto es fácil de hacer usando
# diccionarios:

binary_ops = {
  '+' : 'add',
  '-' : 'sub',
  '*' : 'mul',
  '/' : 'div',
  '<' : 'lt',
  '>' : 'gt',
  '==': 'eq',
  '!=': 'ne',
  '<=': 'le',
  '>=': 'ge',
  'and': 'land',
  'or': 'lor',
}

unary_ops = {
  '+' : 'uadd',
  '-' : 'usub',
  'not' : 'lnot',
}

# PASO 2: Implementar la siguiente clase Visitor Node que creará una
# una secuencia de instrucciones SSA en forma de tuplas. Use la
# decripción anterior de los op-codes permitidos como una guia.
class GenerateCode(mpasast.NodeVisitor):
  '''
  Clase Visitor Node que crea secuencias de instrucciones de 3-direcciones.
  '''
  def __init__(self):
    super(GenerateCode, self).__init__()

    # version diccionario para temporales
    self.versions = defaultdict(int)

    # El código generado (lista de tuplas)
    self.code = BasicBlock()
    self.start_block = self.code

    # Una lista de declaraciones externas (y tipos)
    self.externs = []

  def new_temp(self,typeobj):
    '''
    Crea una nueva variable temporal de un tipo dado.
    '''
    name = "__%s_%d" % (typeobj.name, self.versions[typeobj.name])
    self.versions[typeobj.name] += 1
    return name

  # Debe implementar métodos visit_Nodename para todos los demas nodos
  # del AST.  En su código, se tendrá que hacer las instrucciones y
  # agregarlas a la lista self.code.
  #
  # Siguen algunos métodos de ejemplo.  Deberá ajustarlos dependiendo
  # de los nombres de los nodos AST que se haya definido.

  def visit_Literal(self,node):
    # Crea un nuevo nombre de variable temporal
    target = self.new_temp(node.type)

    # Crea el opcode SSA y lo agrega a la lista de instrucciones generadas
    inst = ('literal_'+node.type.name, node.value, target)
    self.code.append(inst)

    # Graba el nombre de la variable temporal donde el valor fue colocado
    node.gen_location = target

  def visit_BinaryOp(self,node):
    # Visita las expresiones izquierda y derecha
    self.visit(node.left)
    self.visit(node.right)

    # Crea un nuevo temporal para almacenar el resultado
    target = self.new_temp(node.type)

    # Crea opcode y agrega a la lista
    opcode = binary_ops[node.op] + "_"+node.left.type.name
    inst = (opcode, node.left.gen_location, node.right.gen_location, target)
    self.code.append(inst)

    # Almacena localizacion del resultado en el nodo
    node.gen_location = target

  def visit_Relation(self,node):
    # Visit las expresiones izquierda y derecha
    self.visit(node.left)
    self.visit(node.right)

    # Cree un temporal nuevo para almacer el resultado
    target = self.new_temp(node.type)

    # Cree el opcode y agregarlo a la lista
    #opcode = binary_ops[node.op] + "_"+node.left.type.name
    opcode = "cmp" + "_"+node.left.type.name
    inst = (opcode, binary_ops[node.op], node.left.gen_location, node.right.gen_location, target)
    self.code.append(inst)

    # Almacene localizacion del resultado al nodo
    node.gen_location = target

  def visit_Print(self,node):
    # Visit la expresion print
    self.visit(node.literal)

    # Cree el opcode y agregarlo a la lista
    inst = ('print_literal', node.literal.gen_location)
    self.code.append(inst)

  def visit_Write(self,node):
    self.visit(node.expression)

    inst = ('print_'+node.expression.type.name, node.expression.gen_location)
    self.code.append(inst)

  def visit_Read(self,node):
    self.visit(node.location)

    inst = ('read_'+node.location.type.name, node.location.gen_location)
    self.code.append(inst)

#  def visit_Program(self,node):
#    self.visit(node.program)

  #def visit_Statements(self,node):
  #    self.visit(node.expr)
  #    inst = ('print_'+node.expr.type.name, node.expr.gen_location)
  #    self.code.append(inst)

  #def visit_Statement(self,node):
  #    self.visit(node.expr)
  #    inst = ('print_'+node.expr.type.name, node.expr.gen_location)
  #    self.code.append(inst)

  def visit_Parameters_Declaration(self,node):
    inst = ('alloc_'+node.type.name, 
            node.id)
    self.code.append(inst)

  def visit_Local(self,node):
    inst = ('alloc_'+node.type.name, 
            node.id)
    self.code.append(inst)

  def visit_Location(self,node):
    target = self.new_temp(node.type) 
    if node.pos:
      inst = ('load_'+node.type.name,
            node.id, target + " + " + node.pos)
    else:
      inst = ('load_'+node.type.name,
            node.id, target)
    self.code.append(inst)
    node.gen_location = target


    def visit_Cast(self,node):
      target = self.new_temp(node.type)
      inst = ('move', node.gen_location, target)
      self.code.append(inst)
      node.gen_location = target

  def visit_Assignment(self,node):
    self.visit(node.expression)
    inst = ('store_'+node.expression.type.name, 
            node.expression.gen_location, 
            node.location)
    self.code.append(inst)

  def visit_UnaryOp(self,node):
    self.visit(node.left)
    target = self.new_temp(node.type)
    opcode = unary_ops[node.op] + "_" + node.left.type.name
    inst = (opcode, node.left.gen_location)
    self.code.append(inst)
    node.gen_location = target

  def visit_IfStatement(self,node):
    if_block = IfBlock()
    self.code.next_block = if_block
    # condition
    self.switch_block(if_block)
    self.visit(node.cond)
    if_block.test = node.cond.gen_location
    # then branch
    if_block.if_branch = BasicBlock()
    self.switch_block(if_block.if_branch)
    self.visit(node.then_b)
    # else branch
    if node.else_b:
        if_block.else_branch = BasicBlock()
        self.switch_block(if_block.else_branch)
        self.visit(node.else_b)
    # fija el siguiente bloque
    if_block.next_block = BasicBlock()
    self.switch_block(if_block.next_block)

  def visit_WhileStatement(self, node):
    while_block = WhileBlock()
    self.code.next_block = while_block
    # condition
    self.switch_block(while_block)
    self.visit(node.cond)
    while_block.test = node.cond.gen_location
    # body
    while_block.body = BasicBlock()
    self.switch_block(while_block.body)
    self.visit(node.body)
    while_block.next_block = BasicBlock()
    self.switch_block(while_block.next_block)

  def switch_block(self, next_block):
    self.code = next_block

  def visit_Group(self,node):
    self.visit(node.expression)
    node.gen_location = node.expression.gen_location

  # def visit_FunCall(self,node):
  #     self.visit(node.expr)
  #     inst = ('print_'+node.expr.type.name, node.expr.gen_location)
  #     self.code.append(inst)


# STEP 3: Probar
# 
# Trate de correr este programa con un archivo adecuado para tal efecto y vea
# la secuencia del codigo SSA resultante.
#
#     bash % python mpascode.py good.pas
#     ... vea la salida ...
#
# ----------------------------------------------------------------------
#            NO MODIFIQUE NADA DE AQUI EN ADELANTE
# ----------------------------------------------------------------------
def generate_code(node):
  '''
  Genera código SSA desde el nodo AST entregado.
  '''
  gen = GenerateCode()
  gen.visit(node)
  return gen

if __name__ == '__main__':
  import mpaslex
  import mpasparse
  import mpascheck
  import sys
  from errors import subscribe_errors, errors_reported
  lexer = mpaslex.make_lexer()
  parser = mpasparse.make_parser()
  with subscribe_errors(lambda msg: sys.stdout.write(msg+"\n")):
    program = parser.parse(open(sys.argv[1]).read())
    # Revise el programa
    mpascheck.check_program(program)
    # Si no ocurre errore, genere código
    if not errors_reported():
      code = generate_code(program)
      # Emite la secuencia de código
      mpasblock.PrintBlocks().visit(code.start_block)
      #for inst in code.code:
      #    print(inst)
