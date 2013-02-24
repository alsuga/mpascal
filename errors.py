# errors.py
'''
Soporte al manejo de errores del Compilador.

Una de las partes mas importantes (y dificiles) de escribir un compilador
es un reporte confiable de mensajes de error al usuario.  Este archivo
define alguna funcionalidad generica para tratar con errores a traves
del proyecto del compilador.  El manejo de errores se basa en un enfoque
suscripcion/registro (subscription/logging based approach).

Para reportar un error en el compilador, use la funcion error(). Por ejemplo:

       error(lineno,"Alguna clase de mensaje de error del compilador")

donde lineno es el numero de la linea en la cual ocurrio el error.  Si su
compilador soporta multiples archivos fuentes, agrege el argumento clave filename.

       error(lineno,"Alguna clase de mensaje de error del compilador",filename="foo.src")

El manejo de errores es basado en el modelo base de suscripcion usando
manejadores-contexto y la funcion subscribe_errors(). Por ejemplo, para enrutar
el mensaje de error a la salida estandar, use esto:

       with subscribe_errors(print):
            run_compiler()

Para enviar el mensaje al error estandar, usted puede hacer esto:

       import sys
       from functools import partial
       with subscribe_errors(partial(print,file=sys.stderr)):
            run_compiler()

Para enrutar el mensaje a un registro, usted puede hacer esto:

       import logging
       log = logging.getLogger("somelogger")
       with subscribe_errors(log.error):
            run_compiler()

Para recoger mensajes de error para el proposito de pruebas unitarias, haga esto:

       errs = []
       with subscribe_errors(errs.append):
            run_compiler()
       # Comprobar errs para errores especificos

La funcion de utilidad errors_reported() devuelve el numero total de
errores reportados hasta el momento.  Las diferentes estapas del compilador
podrian utilizar esto para decidir si se continua o no con el proceso.

Utilice clear_errors() para borrar el numero total de errores.
'''

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
