# mpasblock.py
# -*- coding: utf-8 -*-
'''
Bloques Basicos y Control de Flujo
----------------------------------------
Este archivo define clases y funciones para crear y recorrer
bloques básicos.  Deberá escribir el código que sea necesario
para sus necesidades.
'''

# blocks.py
#
# Un ejemplo de como crear bloques básicos, grafos de control de flujo
# y codigo de bajo-nivel usando el AST de Python.

binary_ops = {
  '+' : 'ADD',
  '-' : 'SUB',
  '*' : 'MUL',
  '/' : 'DIV',
  '<' : 'L',
  '>' : 'G',
  '==': 'EQ',
  '!=': 'NE',
  '<=': 'LE',
  '>=': 'GE',
  'and': 'AND',
  'or': 'OR',
}

unary_ops = {
  '+' : 'uadd',
  '-' : 'usub',
  'not' : 'lnot',
}


class Block(object):
  def __init__(self):
    self.instructions = []   # Instrucciones en el bloque
    self.next_block = None   # Enlace al siguiente bloque

  def append(self,instr):
    self.instructions.append(instr)

  def __iter__(self):
    return iter(self.instructions)

class BasicBlock(Block):
  '''
  Clase para un simple bloque.  Control de flujo incondicionalmente
  fluye al siguiente bloque.
  '''
  pass

class IfBlock(Block):
  '''
  Clase para un bloque basico representando un if-the-else.  Hay dos
  ramas para manejar cada posibilidad.
  '''
  def __init__(self):
    super(IfBlock,self).__init__()
    self.if_branch = None
    self.else_branch = None
    self.test = None

class WhileBlock(Block):
  def __init__(self):
    super(WhileBlock, self).__init__()
    self.cond = None
    self.body = None

class BlockVisitor(object):
  '''
  Clase para visitar bloques básicos.  Defina una subclase y defina
  métodos tales como visit_BasicBlock o visit_IfBlock para implementar
  procesamiento personalizado (similar a ASTs).
  '''
  def visit(self,block):
    while isinstance(block,Block):
      name = "visit_%s" % type(block).__name__
      if hasattr(self,name):
        getattr(self,name)(block)
      block = block.next_block

import mpasast
class CodeGenerator(mpasast.NodeVisitor):
  '''
  Simple codigo generador con bloques basicos y grafo de control de flujo
  '''
  def __init__(self):
    self.current_block = BasicBlock()
    self.start_block = self.current_block
    self.current_if = 0
    self.current_while = 0
    self.current_fun = 0

  def visit_IfStatement(self,node):
    '''
    Ejemplo de compilacion de la instruncción if Python.  Le
    gustará dibujar una gráfica del enlace.
    '''
    # Paso 1: Cree un nuevo BasicBlock para la condicion de prueba
    ifblock = IfBlock()
    self.current_block.next_block = ifblock
    self.current_block = ifblock

    # Paso 2:  Evalue la condicion de prueba
    self.visit(node.cond)

    # Paso 3: Cree la rama para el if-body
    self.current_block = BasicBlock()
    ifblock.if_branch = self.current_block

    # Paso 4: Recorra todas las instrucciones del if-body
    for bnode in node.then_b:
      self.visit(bnode)

    # Paso 5: Si hay clausula else, cree un nuevo bloque y recorra las instrucciones
    if node.else_b:
      self.current_block = BasicBlock()
      ifblock.else_branch = self.current_block

      # Visite el cuerpo de la clausula else
      for bnode in node.else_b:
        self.visit(bnode)

    # paso 6: Cree un nuevo bloque básico para iniciar la seccion siguiente    
    self.current_block = BasicBlock()
    ifblock.next_block = self.current_block
   
	def visit_Funcdecl(self,node):
		inst = (node.id + str(self.current_fun))
		self.current_fun += 1
    self.current_block.append(inst)
    inst = ("SAVE")
    self.current_block.append(inst)
    self.visit(node.parameters)
    self.visit(node.locals)
    self.visit(node.statements)
    inst = ("RESTORE")
    self.current_block.append(inst)
    inst = ("JMPL", "%i7 + 8")
    self.current_block.append(inst)

  def visit_BinaryOp(self,node):
    self.visit(node.left)
    self.visit(node.right)
    opname = node.op.__class__.__name__
    inst = ("BINARY_"+opname.upper(),)
    self.current_block.append(inst)

  def visit_Relation(self,node):
    self.visit(node.left)
    opname = node.ops[0].__class__.__name__
    self.visit(node.comparators[0])
    inst = ("BINARY_"+opname.upper(),)
    self.current_block.append(inst)

  def visit_Print(self,node):
  	self.visit(node.literal)
  	inst = ("MOVE" , "%i0", "%o0")
  	self.current_block.append(inst)
  	inst = ("CALL", "print")
    self.current_block.append(inst)
    inst = ("NOP",)
    self.current_block.append(inst)

  def visit_Write(self,node):
  	self.visit(node.expression)
  	inst = ("MOVE", "%i0", "%o0")
  	self.current_block.append(inst)
  	inst = ("CALL", "write")
  	self.current_block.append(inst)
  	inst = ("NOP",)
  	self.current_block.append(inst)

  def visit_Read(self,node):
  	self.visit(node.location)
  	inst = ("MOVE", "%i0", "%o0")
  	self.current_block.append(inst)
  	inst = ("CALL", "read")
  	self.current_block.append(inst)
  	inst = ("NOP",)
  	self.current_block.append(inst)

  def visit_FunCall(self,node):
  	self.visit(node.parameters)
  	inst = ("CALL", node.id)
  	self.current_block.append(inst)
  	inst = ("NOP",)
  	self.current_block.append(inst)

#  def visit_ExprList(self,node):
#  	for i in 

class PrintBlocks(BlockVisitor):
  def visit_BasicBlock(self,block):
    print("Block:[%s]" % block.__class__.__name__)
    for inst in block.instructions:
      print("    %s" % (inst,))
    print("")

  def visit_IfBlock(self,block):
    self.visit_BasicBlock(block)
    self.visit(block.if_branch)
    self.visit(block.else_branch)

  def visit_WhileBlock(self, block):
    self.visit_BasicBlock(block)
    self.visit(block.body)

class EmitBlocks(BlockVisitor):
  def visit_BasicBlock(self,block):
    print("Block:[%s]" % block.__class__.__name__)
    for inst in block.instructions:
      print("    %s" % (inst,))

  def visit_IfBlock(self,block):
    self.visit_BasicBlock(block)
    # Emite un salto condicional alrededor del if-branch
    inst = ('JUMP_IF_FALSE',
            block.else_branch if block.else_branch else block.next_block)
    print("    %s" % (inst,))
    self.visit(block.if_branch)
    if block.else_branch:
      # Emite un salto alrededor del if-branch (si hay alguno)
      inst = ('JUMP', block.next_block)
      print("    %s" % (inst,))
      self.visit(block.else_branch)

if __name__ == '__main__':
  import mpaslex
  import mpasparse
  import mpascheck
  import sys
  from errors import subscribe_errors, errors_reported
  lexer = mpaslex.make_lexer()
  parser = mpasparse.make_parser()
  gen = CodeGenerator()
  with subscribe_errors(lambda msg: sys.stdout.write(msg+"\n")):
    program = parser.parse(open(sys.argv[1]).read())
    mpascheck.check_program(program)
    if not errors_reported():
      gen.visit(program)
      EmitBlocks().visit(gen.start_block)



#   top = ast.parse("""\
# start
# if a < 0:
#    a + b
# else:
#    a - b
# done
# """)
#   gen = CodeGenerator()
#   gen.visit(top)

# #    PrintBlocks().visit(gen.start_block)
#   EmitBlocks().visit(gen.start_block)
