from ply import lex

# Lista de tokens
tokens = [
    'SEQ', 'PAR', 'IF', 'ELSE', 'WHILE', 'C_CHANNEL',
    'SEND', 'RECEIVE', 'INPUT', 'OUTPUT', 'IDENTIFIER', 
    'ASSIGN', 'PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE', 
    'STRING', 'COMMA', 'GT', 'LT', 'GE', 'LE', 
    'EQ', 'NE', 'NUMBER', 'LPAREN', 'RPAREN', 
    'LBRACE', 'RBRACE', 'SEMICOLON', 'BOOL'
]

# Regras de palavras-chave
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
t_ID = r'[a-zA-Z_][a-zA-Z0-9_]*'  # Identificadores, incluindo palavras reservadas

# Função de erro para tokens não reconhecidos
def t_error(t):
    print(f"Caractere ilegal {t.value[0]}")
    t.lexer.skip(1)

# Regras mais complexas
def t_NUMBER(t):
    r'\d+'  # Números inteiros
    t.value = int(t.value)  # Converte para número
    return t

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'  # Identificadores válidos
    t.type = reserved.get(t.value, 'IDENTIFIER')  # Checa se é uma palavra reservada
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
