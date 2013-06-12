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
		self.test = None
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

	def visit_If(self,node):
		'''
		Ejemplo de compilacion de la instruncción if Python.  Le
		gustará dibujar una gráfica del enlace.
		'''
		# Paso 1: Cree un nuevo BasicBlock para la condicion de prueba
		ifblock = IfBlock()
		self.current_block.next_block = ifblock
		self.current_block = ifblock

		# Paso 2:  Evalue la condicion de prueba
		self.visit(node.test)

		# Paso 3: Cree la rama para el if-body
		self.current_block = BasicBlock()
		ifblock.if_branch = self.current_block

		# Paso 4: Recorra todas las instrucciones del if-body
		for bnode in node.body:
			self.visit(bnode)

		# Paso 5: Si hay clausula else, cree un nuevo bloque y recorra las instrucciones
		if node.orelse:
			self.current_block = BasicBlock()
			ifblock.else_branch = self.current_block

			# Visite el cuerpo de la clausula else
			for bnode in node.orelse:
				self.visit(bnode)

		# paso 6: Cree un nuevo bloque básico para iniciar la seccion siguiente		
		self.current_block = BasicBlock()
		ifblock.next_block = self.current_block
		
	def visit_BinOp(self,node):
		self.visit(node.left)
		self.visit(node.right)
		opname = node.op.__class__.__name__
		inst = ("BINARY_"+opname.upper(),)
		self.current_block.append(inst)

	def visit_Compare(self,node):
		self.visit(node.left)
		opname = node.ops[0].__class__.__name__
		self.visit(node.comparators[0])
		inst = ("BINARY_"+opname.upper(),)
		self.current_block.append(inst)

	def visit_Name(self,node):
		if isinstance(node.ctx, ast.Load):
			inst = ('LOAD_GLOBAL',node.id)
		else:
			inst = ('Unimplemented,')
		self.current_block.append(inst)

	def visit_Num(self,node):
		inst = ('LOAD_CONST',node.n)
		self.current_block.append(inst)

class PrintBlocks(BlockVisitor):
	def visit_BasicBlock(self,block):
		print("Block:[%s]" % block)
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
		print("Block:[%s]" % block)
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
	top = ast.parse("""\
start
if a < 0:
   a + b
else:
   a - b
done
""")
	gen = CodeGenerator()
	gen.visit(top)

#    PrintBlocks().visit(gen.start_block)
	EmitBlocks().visit(gen.start_block)
