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
    ('right', 'ELSE'),
)

def p_program(p):
    '''
    program : program function
            | function 
    '''
    if len(p) == 3 :
        p[0] = Program([p[1]])
        p[0].append(p[2])
    else:
        p[0] = Program([p[1]])

def p_statements(p):
    '''
    statements : statement
               | BEGIN st END
    '''
    if len(p) == 2 :
        p[0] = p[1]
    else:
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
            | read
    '''
    p[0] = Statement(p[1])

#def p_const_declaration(p):
#    '''
#    const_declaration : CONST id ASSIGN expression SEMI
#    '''
#    p[0] = ConstDeclaration(p[2],p[4])

def p_locals(p):
    '''
    locals : locals local
    '''
    p[0] = Locals([p[1]])
    p[0].append(p[2])

def p_locals_1(p):
    '''
    locals : empty
    '''
    p[0] = p[1]

def p_local(p):
    '''
    local : id COLON typename SEMI
    '''
    p[0] = Local(p[1], p[3])

def p_local_2(p):
    '''
    local : id COLON typename LBRACKET literal RBRACKET SEMI 
    '''
    p[0] = Local_vec(p[1], p[3], p[5])

def p_fundecl(p):
    '''
    function : FUNC id LPAREN parameters RPAREN locals BEGIN statements END
    '''
    p[0] = Funcdecl(p[2], p[4], p[6], p[8]) 

def p_parameters(p):
    '''
    parameters : parameters COMMA parm_declaration
    '''
    p[0] = Parameters([p[1]])
    p[0].append(p[3])

def p_parameters_1(p):
    '''
    parameters : parm_declaration
               | empty
    '''
    p[0] = p[1]

def p_parm_declaration(p):
    '''
    parm_declaration : id COLON typename
    '''
    p[0] = Parameters_Declaration(p[1], p[3])

def p_parm_declaration_1(p):
    '''
    parm_declaration : id COLON typename LBRACKET literal RBRACKET
    '''
    p[0] = Parameters_Declaration_vec(p[1], p[3], p[5])

def p_assign(p):
    '''
    assign : id ASSIGN expression SEMI 
    '''
    p[0] = Assignment(p[1], p[3])

def p_print(p):
    '''
    print : PRINT LPAREN expression RPAREN SEMI
    '''
    p[0] = Print(p[3])

def p_read(p):
    '''
    read : READ LPAREN id RPAREN SEMI
    '''
    p[0] = Read(p[3])

def p_expression_unary(p):
    '''
    expression :  PLUS expression %prec UNARY
                |  MINUS expression %prec UNARY
    '''
    p[0] = UnaryOp(p[1], p[2])


def p_expression_group(p):
    '''
    expression : LPAREN expression RPAREN
    '''
    p[0] = Group(p[2])

def p_expression_funcall(p):
    '''
    expression :  id LPAREN exprlist RPAREN 
                | id LPAREN RPAREN
    '''
    if len(p == 5):
        p[0] = FunCall(p[1], p[3])
    else:
        p[0] = FunCall_v(p[1])

def p_if(p):
    '''
    if : IF cond THEN statements %prec ELSE
    '''
    p[0] = IfStatement(p[2], p[4])

def p_if_else(p):
    '''
    if_else :  IF cond THEN statements ELSE statements
    '''
    p[0] = If_elseStatement(p[2], p[4], p[6])

def p_while(p):
    '''
    while : WHILE cond statements
    '''
    p[0] = WhileStatement(p[2], p[3])

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
        else :
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
    cond : id
          | literal
    ''' 
    p[0] = p[1]

def p_expression_1(p):
    '''
    expression : id 
                | literal
    '''
    p[0] = p[1]

def p_expression_2(p):
    '''
    expression : typename LPAREN id RPAREN 
    '''
    p[0] = Cast(p[1],p[3])

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
    p[0] = Literal(p[1])

def p_typename(p):
    '''
    typename : TYPENAME
    '''
    p[0] = Typename(p[1])

def p_id(p):
    '''
    id : ID
    '''
    p[0] = Id(p[1])

def p_id_2(p):
    '''
    id : ID LBRACKET expression RBRACKET
    '''
    p[0] = Id_vec(p[1],p[3])

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

def dump_tree(node, indent = ""):
    #print node
    if not hasattr(node, "datatype"):
        datatype = ""
    else:
        datatype = node.datatype

    if(node.__class__.__name__ != "str" and node.__class__.__name__ != "list"):
        print "%s%s  %s" % (indent, node.__class__.__name__, datatype)

    indent = indent.replace("-"," ")
    indent = indent.replace("+"," ")
    if hasattr(node,'_fields'):
        mio = node._fields
    else:
        mio = node
    if(isinstance(mio,list)):
        for i in range(len(mio)):
            if(isinstance(mio[i],str) ):
                c = getattr(node,mio[i])
            else:
             c = mio[i]
            if i == len(mio)-1:
                dump_tree(c, indent + "  +-- ")
            else:
                dump_tree(c, indent + "  |-- ")
    else:
        print indent, mio


if __name__ == '__main__':
    import mpaslex
    import sys
    from errors import subscribe_errors
    lexer = mpaslex.make_lexer()
    parser = make_parser()
    with subscribe_errors(lambda msg: sys.stdout.write(msg+"\n")):
        program = parser.parse(open(sys.argv[1]).read())

    dump_tree(program)
    #for depth,node in flatten(program):
    #    dump_tree(node)
        #print("%s%s" % (" "*(4*depth),node.__class__.__name__))