from ply import yacc
from errors import error
from mpaslex import tokens
from mpasast import *

precedence = (
    ('left', 'LOR'),
    ('left', 'LAND'),
    ('nonassoc', 'LT', 'LE', 'EQ', 'GT', 'GE', 'NE'),
    ('left', 'PLUS', "MINUS"),
    ('left', "TIMES", "DIVIDE"),
    ('right', 'UNARY'),  
)


def p_program(p):
    '''program : program function 
                | empty
    '''
    p[0] = p[1]
    p[0].append(p[2])

def p_statements(p):
    '''
    statements : statement
               | BEGIN st END
    '''
    p[0] = p[1]
    p[0] = p[2]

def p_st(p):
    '''
    st : st statement
       | empty
    '''
    p[0] = p[1]
    p[0].append(p[2])



def p_statement(p):
    '''
    statement : assign
            | print
            | if
            | if_else
            | while
            | BREAK
    '''
    p[0] = Statement(p[1])

#def p_const_declaration(p):
#    '''
#    const_declaration : CONST ID ASSIGN expression SEMI
#    '''
#    p[0] = ConstDeclaration(p[2],p[4])
 
def p_locals(p):
    '''
    locals : locals ID COLON typename SEMI
            | empty
    '''
    p[0] = VarDeclaration(p[2], p[3], None, lineno=p.lineno(2))


def p_fundecl(p):
    '''function : FUNC ID LPAREN parameters RPAREN locals BEGIN statements END'''
    p[0] = Funcdecl(ID = p[2], param_list = p[4], locals = p[6], statements = p[8]) 

def p_parameters(p):
    '''
    parameters : parameters COMMA parm_declaration
    '''
    p[0] = p[1]
    p[0].append(p[3])

def p_parameters_1(p):
    '''
    parameters : parm_declaration
               | empty
    '''
    p[0] = Parameters([p[1]])

def p_parm_declaration(p):
    '''
    parm_declaration : ID typename
    '''
    p[0] = ParamDecl(p[1], p[2])

def p_assign(p):
    '''
    assign : ID ASSIGN expression SEMI 
    '''
    p[0] = AssignmentStatement(p[1], p[3])

def p_print(p):
    '''
    print : PRINT expression SEMI
    '''
    #import pydb; pydb.debugger()
    p[0] = PrintStatement(p[2])


def p_expression_unary(p):
    '''
    expression :  PLUS expression %prec UNARY
                |  MINUS expression %prec UNARY
    '''
    p[0] = UnaryOp(p[1], p[2], lineno=p.lineno(1))


def p_expression_group(p):
    '''
    expression : LPAREN expression RPAREN
    '''
    p[0] = Group(p[2])

def p_expression_funcall(p):
    '''
    expression :  ID LPAREN exprlist RPAREN 
                | ID LPAREN RPAREN
    '''
    if len(p == 5):
        p[0] = FunCall(p[1], [2])
    else:
        p[0] = FunCall(p[1],[])

def p_if(p):
    '''
    if : IF cond THEN statements
    '''
    p[0] = IfStatement(p[2], p[4], None)

def p_if_else(p):
    '''
    if_else :  IF cond THEN statements ELSE statements
    '''
    p[0] = IfStatement(p[2], p[4], p[8])

def p_while(p):
    '''
    while : WHILE cond statements
    '''
    p[0] = WhileStatement(p[2], p[4])

def p_expression(p):
    '''
    expression : expression PLUS expression
                | expression MINUS expression
                | expression TIMES expression
                | expression DIVIDE expression
    '''
    if (len (p) == 4):
        if(p[2] == '+' ):
            p[0] = BinaryOp("+",p[1],p[3])
        elif (p[2] == '-'):
            p[0] = BinaryOp("-",p[1],p[3])
        elif (p[2] == '*' ):
            p[0] = BinaryOp("*",p[1],p[3])
        elif (p[2] == '/'):
            p[0] = BinaryOp("/",p[1],p[3])

def p_comp(p):
    '''
    cond : expression LT expression
         | expression GT expression
         | expression LE expression
         | expression GE expression
         | expression EQ expression
         | expression NE expression
    '''
    if (len (p) == 4):
        if(p[2] == '<' ):
            p[0] = BinaryOp("<",p[1],p[3])
        elif (p[2] == '>'):
            p[0] = BinaryOp(">",p[1],p[3])
        elif (p[2] == '<=' ):
            p[0] = BinaryOp("<=",p[1],p[3])
        elif (p[2] == '>='):
            p[0] = BinaryOp(">=",p[1],p[3])
        elif (p[2] == '=='):
            p[0] = BinaryOp("==",p[1],p[3])
        else:
            p[0] = BinaryOp("!=",p[1],p[3])

    
def p_cond(p):
    '''
    cond : cond LAND cond
         | cond LOR cond
         |  LNOT cond %prec UNARY
    '''
    if( len(p) == 4):
        if(p[2] == 'or' ):
            p[0] = BinaryOp('or', p[1], p[3])
        else:
            p[0] = BinaryOp('and', p[1], p[3])
    elif (len(p) == 3):
        p[0] = UnaryOp('not',p[2])

def p_cond_1(p):
    '''
    cond : ID
          | literal
    ''' 


def p_expression_1(p):
    '''
    expression : ID 
                | literal
    '''
    p[0] = p[1]


def p_exprlist(p):
    '''
    exprlist :  exprlist COMMA expression
    '''
    p[0] = p[1]
    p[0].append(p[3])

def p_exprlist_1(p):
    '''
    exprlist : expression
    '''
    p[0] = ExprList([p[1]])

def p_literal(p):
    '''
    literal : INTEGER
            | FLOAT
            | STRING
            | BOOLEAN
    '''
    p[0] = Literal(p[1],lineno=p.lineno(1))


def p_typename(p):
    '''
    typename : ID
    '''
    p[0] = p[1]

def p_empty(p):
    '''
    empty    :
    '''
    pass


def p_error(p):
    if p:
        error(p.lineno, "Error de sintaxis en el token '%s'" % p.value)
    else:
        error("EOF","Error de sintaxis, fin de entrada.")

def make_parser():
    parser = yacc.yacc()
    return parser

if __name__ == '__main__':
    import mpaslex
    import sys
    from errors import subscribe_errors
    lexer = mpaslex.make_lexer()
    parser = make_parser()
    with subscribe_errors(lambda msg: sys.stdout.write(msg+"\n")):
        program = parser.parse(open(sys.argv[1]).read(),debug = 1)

    for depth,node in flatten(program):
        print("%s%s" % (" "*(4*depth),node))