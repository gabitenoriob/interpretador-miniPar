#Gramática
# programa_minipar ::= bloco_stmt
# bloco_stmt ::= bloco_SEQ | bloco_PAR
# bloco_SEQ ::= SEQ stmts
# bloco_PAR ::= PAR stmts
# stmts ::= atribuição | if ( bool ) stmt | if ( bool ) stmt else stmt | while ( bool ) stmt
# atribuição ::= id = expr
# expr ::= c_channel chan id id_comp1 id_comp2


import re

# Definindo os tipos de tokens
TOKENS = {
    'SEQ': r'SEQ',
    'PAR': r'PAR',
    'IF': r'\bif\b',
    'ELSE': r'\belse\b',
    'WHILE': r'\bwhile\b',
    'BOOL': r'\b(Bool)\b',
    'C_CHANNEL': r'\bc_channel\b',
    'SEND': r'\bsend\b',
    'RECEIVE': r'\breceive\b',
    'IDENTIFIER': r'[a-zA-Z_][a-zA-Z0-9_]*',
    'ASSIGN': r'=',
    'PLUS': r'\+',
    'MINUS': r'-',
    'MULTIPLY': r'\*',
    'DIVIDE': r'/',
    'STRING': r'"[^"\n]*"',  
    'COMMA': r',', 
    'GT': r'>',  # Operador 'maior que'
    'LT': r'<',  # Operador 'menor que'
    'GE': r'>=',  # Operador 'maior ou igual a'
    'LE': r'<=',  # Operador 'menor ou igual a'
    'EQ': r'==',  # Operador 'igual a'
    'NE': r'!=',  # Operador 'diferente de'
    'WHITESPACE': r'\s+',
    'COMMENT': r'#[^\n]*',
    'NUMBER': r'\d+',
    'LPAREN': r'\(',
    'RPAREN': r'\)',
    'LBRACE': r'{',
    'RBRACE': r'}',
    'SEMICOLON': r';',
    'INVALID': r'.'
}



# Compilando expressões regulares
token_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKENS.items())
compiled_regex = re.compile(token_regex)

def tokenize(code):
    """Tokeniza o código MiniPar em uma lista de tokens."""
    tokens = []
    line_number = 1

    for match in compiled_regex.finditer(code):
        kind = match.lastgroup
        value = match.group()

        if kind == 'WHITESPACE':
            continue
        elif kind == 'COMMENT':
            continue
        elif kind == 'INVALID':
            raise ValueError(f"Erro léxico na linha {line_number}: token inválido '{value}'")
        elif kind == 'IDENTIFIER':
            # Se o identificador for uma palavra-chave, atualiza o tipo
            if value in TOKENS.keys():
                kind = value
        tokens.append((kind, value))
    
    return tokens


