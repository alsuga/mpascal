

def generate(file,top):
  print >>file, "! Creado por mpascal.py"
  print >>file, "! Alejandro Suarez- David Escobar, IS744 (2013-1)"

def emit_program(out,top):
  print >>out,"\n! program"
  for i in top.function:
    emit_function(out,i)

def emit_function(out,func):
  print >>out,"\n! function: %s (start) " % func.id
  #print >>out,"    .global %s \n" % func.id
  #print >>out,"%s: \n" % func.id
  #label = new_label()
  #sttms = func.children[2].children
  #args = func.children[0].children
  #local = func.children[1].children
  emit_statements(out, func.statements)
  #print >> out, "\n%s:" % label
  #if func.leaf =="main":
  #  print >> out, "     mov 0, %o0"
  #  print >> out, "     call_exit "
  #  print >> out, "     nop"
  #print >> out, "     ret"
  #print >> out, "     restore"
  print >>out,"\n! function: %s (end) " % func.id

def emit_statements(out,statements):
  for s in statements:
    def emit_statement(out,s):
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

def emit_skip(out,s):
  print >>out, "\n! skip (start)"
  print >>out, "! skip (end)"

def emit_break(out,s):
  print >>out, "\n! break (start)"
  print >>out, "! break (end)"

def emit_assignment(out,s):
  print >>out, "\n! assignment(start)"
  print >>out, "! assignment (end)"

def emit_print(out,s):
  print >>out, "\n! print (start)"
  print >>out, "! print (end)"

def emit_read(out,s):
  print >>out, "\n! read (start)"
  print >>out, "! read (end)"

def emit_write(out,s):
  print >>out, "\n! write (start)"
  print >>out, "! write (end)"

def emit_while(out,s):
  print >>out, "\n! while (start)"
  print >>out, "! while (end)"

def emit_if(out,s):
  print >>out, "\n! if (start)"
  print >>out, "! if (end)"