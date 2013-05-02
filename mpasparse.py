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
        p[1].append(p[2])
        p[0] = p[1]
    else:
        p[0] = Program([p[1]])

#vuelve st para los BEGIN  y END en los while, if y else

def p_st(p):
    '''
    statement : BEGIN statements END
    '''
    p[0] = p[2]

#def p_st_1(p):
#    '''
#    st : statement
#    '''
#    p[0] = p[1]

def p_statements(p):
    '''
    statements : statement
    '''
    p[0] = Statements([p[1]])

# se quito st, entrando en la regla statements 

def p_statements_1(p):
    '''
    statements : statements SEMI statement

    '''
    p[1].append(p[3])
    p[0] = p[1]

def p_statement(p):
    '''
    statement : assign
            | print
            | if
            | if_else
            | while
            | BREAK 
            | SKIP 
            | read
            | write
            | funcall 
            | return
    '''
    if(p[1] == 'skip'):
        p[0] = Skip()
    elif p[1] == 'break':
        p[0] = Break()
    else:
        p[0] = p[1]

#def p_const_declaration(p):
#    '''
#    const_declaration : CONST id ASSIGN expression 
#    '''
#    p[0] = ConstDeclaration(p[2],p[4])

def p_locals(p):
    '''
    locals : locals local
    '''
    p[1].append(p[2])
    p[0] = p[1]

def p_locals_1(p):
    '''
    locals : local
    '''
    p[0] = Locals([p[1]])

def p_local(p):
    '''
    local : ID COLON TYPENAME SEMI
    '''
    p[0] = Local(p[1], p[3],None)

def p_local_1(p):
    '''
    local : ID COLON TYPENAME LBRACKET literal RBRACKET SEMI
    '''
    p[0] = Local(p[1], p[3], p[5])

def p_local_2(p):
    '''
    local : function SEMI
    '''
    p[0] = p[1]

def p_fundecl(p):
    '''
    function : FUNC ID LPAREN parameters RPAREN locals BEGIN statements END
    '''
    p[0] = Funcdecl(p[2], p[4], p[6], p[8]) 

#nueva, no cambia el arbol

def p_fundecl_1(p):
    '''
    function : FUNC ID LPAREN parameters RPAREN BEGIN statements END
    '''
    p[0] = Funcdecl(p[2], p[4], None, p[7]) 

def p_parameters(p):
    '''
    parameters : parameters COMMA parm_declaration
    '''
    p[1].append(p[3])
    p[0] = p[1]

def p_parameters_1(p):
    '''
    parameters : parm_declaration
               | empty
    '''
    p[0] = Parameters([p[1]])

def p_parm_declaration(p):
    '''
    parm_declaration : ID COLON TYPENAME
    '''
    p[0] = Parameters_Declaration(p[1], p[3],None)

def p_parm_declaration_1(p):
    '''
    parm_declaration : ID COLON TYPENAME LBRACKET literal RBRACKET
    '''
    p[0] = Parameters_Declaration(p[1], p[3], p[5])

def p_if(p):
    '''
    if : IF cond THEN statement %prec ELSE
    '''
    p[0] = IfStatement(p[2], p[4], None)

def p_if_else(p):
    '''
    if_else :  IF cond THEN statement ELSE statement
    '''
    p[0] = IfStatement(p[2], p[4], p[6])

def p_while(p):
    '''
    while : WHILE cond DO statement
    '''
    p[0] = WhileStatement(p[2], p[4])

def p_assign(p):
    '''
    assign : location ASSIGN expression  
    '''
    p[0] = Assignment(p[1], p[3])

def p_print(p):
    '''
    print : PRINT LPAREN literals RPAREN 
    '''
    p[0] = Print(p[3])

def p_write(p):
    '''
    write : WRITE LPAREN expression RPAREN 
    '''
    p[0] = Write(p[3])

def p_return(p):
    '''
    return : RETURN expression 
    '''
    p[0] = Return(p[2])

def p_read(p):
    '''
    read : READ LPAREN location RPAREN 
    '''
    p[0] = Read(p[3])


def p_expression_funcall_1(p):
    '''
    funcall :  ID LPAREN exprlist RPAREN 
    '''
    p[0] = FunCall(p[1], p[3])

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
    expression : funcall
    '''
    p[0] = p[1]

def p_expression(p):
    '''
    expression : expression PLUS expression
                | expression MINUS expression
                | expression TIMES expression
                | expression DIVIDE expression
    '''
    
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
            p[0] = Relation('or', p[1], p[3])
        else:
            p[0] = Relation('and', p[1], p[3])
    elif (len(p) == 3):
        p[0] = UnaryOp('not',p[2])

#se omiten los tipos de dato bool por ahora

#def p_cond_1(p):
#    '''
#    cond : id
#          | literal
#    ''' 
#    p[0] = p[1]

#se agregan las agrupaciones de los cond

def p_cond_1(p):
    '''
    cond : LPAREN cond RPAREN
    ''' 
    p[0] = Group(p[2])

def p_expression_1(p):
    '''
    expression : location
                | literal
    '''
    p[0] = p[1]

def p_expression_2(p):
    '''
    expression : TYPENAME LPAREN expression RPAREN 
    '''
    p[0] = Cast(p[1],p[3])

def p_exprlist(p):
    '''
    exprlist :  exprlist COMMA expression
    '''
    p[1].append(p[3])
    p[0] = p[1]

def p_exprlist_1(p):
    '''
    exprlist : expression
            | empty
    '''
    p[0] = ExprList([p[1]])

#se quital los literales bool

def p_literal(p):
    '''
    literal : INTEGER
    '''
    p[0] = Literal("int",p[1])

def p_literal_1(p):
    '''
    literal : FLOAT
    '''
    p[0] = Literal("float",p[1])

def p_literal_2(p):
    '''
    literals : STRING
    '''
    p[0] = Literal("string",p[1])

def p_location(p):
    '''
    location : ID
    '''
    p[0] = Location(p[1],None)

def p_location_2(p):
    '''
    location : ID LBRACKET expression RBRACKET
    '''
    p[0] = Location(p[1],p[3])

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
        program = parser.parse(open(sys.argv[1]).read())
    print "listo parte uno"
    dot = DotVisitor()
    dot.visit(program)
    print "listo visitado"
    dot.graph.write_png("grafo.png")

    #dump_tree(program)
    #for depth,node in flatten(program):
    #    print("%s%s" % (" "*(4*depth),node.__class__.__name__))