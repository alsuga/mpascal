import StringIO
data = StringIO.StringIO()

bin_ops = {
  '+' : 'ADD',
  '-' : 'SUB',
  '*' : 'MUL',
  '/' : 'DIV',
  '<' : 'LW',
  '>' : 'GT',
  '==': 'EQ',
  '!=': 'NE',
  '<=': 'LE',
  '>=': 'GE',
  'and': 'AND',
  'or': 'OR',
}

un_ops = {
  '+' : 'uadd',
  '-' : 'usub',
  'not' : 'lnot',
}

cont = -1

def generate(out,top):
  print >>out, "! Creado por mpascal.py"
  print >>out, "! Alejandro Suarez- David Escobar, IS744 (2013-1)"
  print >>out, "   .section     \".text\""
  print >>data,"\n    .section \".rodata\" \n"


def emit_program(out,top):
  print >>out,"\n! program"
  for i in top.function:
    emit_function(out,i)
  print >>out, data.getvalue()


def emit_function(out,func):
  print >>out,"\n! function: %s (start) " % func.id
  print >>out,"    .global %s \n" % func.id
  print >>out,"%s: \n" % func.id
  label = new_label()
  emit_statements(out, func.statements)
  print >> out, "\n%s:" % label
  #if func.leaf =="main":
  #  print >> out, "     mov 0, %o0"
  #  print >> out, "     call_exit "
  #  print >> out, "     nop"
  #print >> out, "     ret"
  #print >> out, "     restore"
  print >>out,"\n! function: %s (end) " % func.id

def emit_statements(out,statements):
  if hasattr(statements,"statements"):
    for s in statements.statements:
      emit_statemet(out,s)
  else:
    emit_statemet(out,statements)

def emit_statemet(out,s):  
  if s.__class__.__name__ == 'Print':
    emit_print(out,s)
  elif s.__class__.__name__ == 'Read':
    emit_read(out,s)
  elif s.__class__.__name__ == 'Write':
    emit_write(out,s)
  elif s.__class__.__name__ == 'IfStatement':
    emit_if(out,s)
  elif s.__class__.__name__ == 'WhileStatement':
    emit_while(out,s)
  elif s.__class__.__name__ == 'Assignment':
    emit_assignment(out,s)
  elif s.__class__.__name__ == 'Skip':
    emit_skip(out,s)
  elif s.__class__.__name__ == 'Break':
    emit_break(out,s)
  elif s.__class__.__name__ == 'Return':
    emit_return(out,s)

def emit_skip(out,s):
  print >>out, "\n! skip (start)"
  print >>out, "! skip (end)"

def emit_break(out,s):
  print >>out, "\n! break (start)"
  print >>out, "! break (end)"

def emit_assignment(out,s):
  print >>out, "\n! assignment(start)"
  eval_expression(out,s.expression)
  print >>out, "!   %s := pop" %s.location.id
  print >>out, "! assignment (end)"

def emit_print(out,s):
  print >>out, "\n! print (start)"
  label = new_label()
  print >> data, '%s:      .asciz "%s" ' % (label, s.literal.value)
  # eval_expression(s.expression)
  # print >>out, "!   expr := pop"
  # print >>out, "!   print(expr)"
  print >>out, "! print (end)"

def emit_read(out,s):
  print >>out, "\n! read (start)"
  print >>out, "! read (end)"

def emit_write(out,s):
  print >>out, "\n! write (start)"
  eval_expression(out,s.expression)
  print >>out, "!   expr := pop"
  print >>out, "!   write(expr)"
  print >>out, "! write (end)"

def emit_while(out,s):
  print >>out, "\n! while (start)"
  test_label= new_label()
  done_label= new_label()
  print >>out, "\n%s:\n" % test_label
  eval_expression(out,s.cond)
  print >>out, "!   relop := pop"
  print >>out, "!   if not relop: goto %s" %done_label
  emit_statements(out,s.body)
  print >>out, "\n!   goto %s" %test_label
  print >>out, "\n%s:\n" % done_label
  print >>out, "! while (end)"

def emit_if(out,s):
  print >>out, "\n! if (start)"
  eval_expression(out,s.cond)
  else_label= new_label()
  next_label= new_label()
  print >>out, "!   relop := pop"
  print >>out, "!   if not relop: goto %s" % else_label
  emit_statements(out,s.then_b)
  print >>out, "\n!   goto %s" %next_label
  print >>out, "\n%s:\n" %else_label
  if s.else_b:
    emit_statements(out,s.else_b)
  print >>out, "\n%s:\n" %next_label
  print >>out, "! if (end)"

def emit_return(out,s):
  print >>out, "\n! return (start)"
  eval_expression(out,s.expression)
  print >>out, "!   ret := pop"
  print >>out, "! return (end)"

def eval_expression(out,expr):
  if expr.__class__.__name__ == "Location":
    if expr.pos:
      print >>out, "!   index := pop" 
      print >>out, "!   push %s[index]" % expr.id
    else:
      print >>out, "!   push %s" %expr.id
  elif expr.__class__.__name__ == "Literal":
    print >>out, "!   push %s" %expr.value
  elif expr.__class__.__name__ == "BinaryOp":
    eval_expression(out,expr.left)
    eval_expression(out,expr.right)
    print >>out, "!   %s" % bin_ops[expr.op]
  elif expr.__class__.__name__ == "UnaryOp":
    eval_expression(our,expr.left)
    print >>out, "!   %s" % un_ops[expr.op]
  elif expr.__class__.__name__ == "Group":
    eval_expression(out,expr.expression)
  elif expr.__class__.__name__ == "FunCall":
    num = 1
    for i in expr.parameters.expressions:
      eval_expression(out,i)
      print >>out, "!   arg%s := pop" % str(num)
      num += 1
    a = "!   push %s(" %expr.id
    for i in xrange(1,num-1):
      a += "arg%s," % str(i)
    if num > 0:
      a+= "arg%s" % str(num-1)
    a += ")"
    print >>out, "%s" % a


def new_label():
  global cont
  cont+=1
  return ".L%s" % cont