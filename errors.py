# errors.py

import sys
from contextlib import contextmanager

_subscribers = []
_num_errors = 0

def error(lineno, message, filename=None):
  '''
  Reporta un error del compilador a todos los suscriptores.
  '''
  global _num_errors
  if not filename:
    errmsg = "{}: {}".format(lineno, message)
  else:
    errmsg = "{}:{}: {}".format(filename,lineno,message)
  for subscriber in _subscribers:
    subscriber(errmsg)
  _num_errors += 1

def errors_reported():
  '''
  Devuelve el numero de errores reportados.
  '''
  return _num_errors

def clear_errors():
  '''
  Limpia el numero total de errores reportados.
  '''
  global _num_errors
  _num_errors = 0

@contextmanager
def subscribe_errors(handler):
  '''
  Gestor de contexto que permite el seguimiento de mensajes de error del compilador.
  Utilicelo como sigue donde handler es un llamador tomando un solo argumento
  el cual es la cadena de mensaje de error:

  with subscribe_errors(handler):
    ... do compiler ops ...
  '''
  _subscribers.append(handler)
  try:
    yield
  finally:
    _subscribers.remove(handler)
