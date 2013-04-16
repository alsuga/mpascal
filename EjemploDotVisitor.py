class visit_Program

def 


class DotVisitor(NodeVisitor):
	def __init__(self):
		self.graph = pydot.Dot(nombre, estilo)
		sel.id = 0
	def Id(self):
		self.id += 1
		return "n%d" %self.id
	def visit_NumNode(self, node):
		name = pydot.Node(self.Id(), style, font)
		name.label(node.value)
		return name

	def visit_BinNode(self, node):
		name = 
		left = visit(node.left)
		right = visit(node.right)

		self.graph.add_edge(pydot.Edge(left, right))

	def __str_(self):
		return self.__class__.__name__

#Para mirar el shift/reduce
debug = true 