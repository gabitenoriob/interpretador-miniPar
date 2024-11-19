#Gramática
# <programa_minipar> ::= <bloco_stmt>
# <bloco_stmt> ::= <bloco_SEQ> | <bloco_PAR>
# <bloco_SEQ> ::= SEQ (<stmts>)
# <bloco_PAR> ::= PAR (<stmts>)
# <stmts> ::= <stmt> | <stmt>; <stmts>
# <stmt> ::= <atribuição> | <if_stmt> | <while_stmt> | <canal_com>
# <atribuição> ::= <id> = <expr>
# <if_stmt> ::= if (<bool>) <stmt> | if (<bool>) <stmt> else <stmt>
# <while_stmt> ::= while (<bool>) <stmt>
# <expr> ::= <termo> | <expr> + <termo> | <expr> - <termo>
# <termo> ::= <fator> | <termo> * <fator> | <termo> / <fator>
# <fator> ::= <id> | <constante>
# <canal_com> ::= c_channel chan <id> <id_comp1> <id_comp2>



from ply import lex

# Lista de tokens, incluindo novos comandos
tokens = [
    'SEQ', 'PAR', 'IF', 'ELSE', 'WHILE', 'C_CHANNEL',
    'SEND', 'RECEIVE', 'INPUT', 'OUTPUT', 'IDENTIFIER', 
    'ASSIGN', 'PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE', 
    'STRING', 'COMMA', 'GT', 'LT', 'GE', 'LE', 
    'EQ', 'NE', 'NUMBER', 'LPAREN', 'RPAREN', 
    'LBRACE', 'RBRACE', 'SEMICOLON', 'BOOL'
]

# Regras de palavras-chave (não podem ser identificadores)
reserved = {
    'SEQ': 'SEQ',
    'PAR': 'PAR',
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'c_channel': 'C_CHANNEL',
    'send': 'SEND',
    'receive': 'RECEIVE',
    'Input': 'INPUT',
    'Output': 'OUTPUT'
}

# Regras regulares simples
t_BOOL = r'\b(True|False)\b'
t_ASSIGN = r'='
t_PLUS = r'\+'
t_MINUS = r'-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'/'
t_COMMA = r','
t_GT = r'>'
t_LT = r'<'
t_GE = r'>='
t_LE = r'<='
t_EQ = r'=='
t_NE = r'!='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'{'
t_RBRACE = r'}'
t_SEMICOLON = r';'
t_STRING = r'"[^"\n]*"'  # Strings entre aspas duplas

# Regras mais complexas
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)  # Converte para número
    return t

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_\.]*'
    t.type = reserved.get(t.value, 'IDENTIFIER')  # Checa palavras-chave
    return t

# Ignorar espaços e tabulações
t_ignore = ' \t'

# Comentários (ignorar)
def t_COMMENT(t):
    r'\#[^\n]*'
    pass

# Contar linhas
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Erros
def t_error(t):
    print(f"Erro léxico na linha {t.lineno}: token inválido '{t.value[0]}'")
    t.lexer.skip(1)

# Construindo o analisador léxico
lexer = lex.lex()
def tokenize(input_string):
    lexer.input(input_string)
    tokens = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        tokens.append(tok)
    return tokens
