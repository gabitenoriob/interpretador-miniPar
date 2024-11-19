import ply.yacc as yacc
from analisadorSemantico import SymbolTable
from analisadorLexico import tokens
import analisadorSemantico,analisadorLexico,analisadorSintatico


# Definindo precedência para operadores
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULTIPLY', 'DIVIDE'),
)


# Definir as regras sintáticas
def p_programa_minipar(p):
    '''programa_minipar : bloco_stmt'''
    p[0] = p[1]

def p_bloco_stmt(p):
    '''bloco_stmt : bloco_SEQ
                  | bloco_PAR
                  | bloco_stmt bloco_SEQ
                  | bloco_stmt bloco_PAR'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = (p[1], p[2])

def p_bloco_SEQ(p):
    '''bloco_SEQ : SEQ stmts'''
    p[0] = ('SEQ', p[2])

def p_bloco_PAR(p):
    '''bloco_PAR : PAR stmts'''
    p[0] = ('PAR', p[2])

def p_bloco_IF(p):
    '''bloco_IF : IF LPAREN bool RPAREN LBRACE stmts RBRACE'''
    p[0] = ('IF', p[3], p[6])

def p_bloco_WHILE(p):
    '''bloco_WHILE : WHILE LPAREN bool RPAREN LBRACE stmts RBRACE'''
    p[0] = ('WHILE', p[3], p[6])

def p_bloco_INPUT(p):
    '''bloco_INPUT : INPUT LPAREN RPAREN'''
    p[0] = ('INPUT')

def p_bloco_OUTPUT(p):
    '''bloco_OUTPUT : OUTPUT LPAREN output_args RPAREN'''
    p[0] = ('OUTPUT', p[3])

def p_output_args(p):
    '''output_args : expr
                   | output_args COMMA expr'''
    if len(p) == 2:
        p[0] = (p[1],)
    else:
        p[0] = p[1] + (p[3],)

def p_stmts(p):
    '''stmts : stmt
             | stmts stmt'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_stmt(p):
    '''stmt : atribuicao
            | bloco_IF
            | bloco_WHILE
            | bloco_INPUT
            | bloco_OUTPUT
            | c_channel
            | c_channel_stmt'''
    p[0] = p[1]

def p_atribuicao(p):
    '''atribuicao : ID EQUALS expr
                  | ID EQUALS STRING
                  | ID EQUALS bloco_INPUT
                  | ID EQUALS receive_stmt'''
                  
    p[0] = ('=', p[1], p[3])
    if p[1] not in symbol_table: 
        symbol_table[p[1]] = p[3]

def p_expr(p):
    '''expr : INT
            | STRING
            | expr PLUS expr
            | expr MINUS expr
            | expr TIMES expr
            | expr DIVIDE expr
            | expr LESS_THAN expr
            | expr GREATER_THAN expr
            | expr LESS_THAN_EQUALS expr
            | expr GREATER_THAN_EQUALS expr
            | expr EQUALS_EQUALS expr
            | expr NOT_EQUALS expr
            '''
 
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = (p[2], p[1], p[3])


def p_termo(p):
    """termo : fator
             | termo MULTIPLY fator
             | termo DIVIDE fator"""
    if len(p) == 2:
        p[0] = ('termo', p[1])
    else:
        p[0] = ('termo', p[1], p[2], p[3])

def p_fator(p):
    """fator : IDENTIFIER
             | NUMBER"""
    p[0] = ('fator', p[1])

def p_canal_com(p):
    "canal_com : C_CHANNEL IDENTIFIER IDENTIFIER IDENTIFIER"
    p[0] = ('canal_com', p[2], p[3], p[4])

# Regra para erro
def p_error(p):
    if p:
        print(f"Erro de sintaxe próximo ao token: {p.type}, valor: {p.value}")
    else:
        print("Erro de sintaxe: fim inesperado de entrada.")

# Construindo o parser
parser = yacc.yacc()

# Função para testar o parser
def parse_program(code):
    result = parser.parse(code)  
    return result


