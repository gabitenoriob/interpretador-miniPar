from analisadorLexico import tokenize

class SymbolTable:
    def __init__(self):
        self.symbols = {}

    def define(self, name, var_type):
        """Define uma nova variável ou canal."""
        if name in self.symbols:
            raise Exception(f"Erro: '{name}' já foi declarado.")
        self.symbols[name] = var_type

    def lookup(self, name):
        """Procura uma variável ou canal na tabela de símbolos."""
        if name not in self.symbols:
            raise Exception(f"Erro: '{name}' não foi declarado.")
        return self.symbols[name]

    def check(self, program):
        """Verifica a semântica do programa."""
        for statement in program:
            token_type = statement[0]
            if token_type == 'IDENTIFIER':
                var_name = statement[1]
                self.lookup(var_name)  # Verifica se a variável foi declarada
            elif token_type in {'SEND', 'RECEIVE'}:
                var_name = statement[1]
                self.lookup(var_name)  # Verifica se o canal foi declarado
            elif token_type in {'IF', 'WHILE'}:
                condition = statement[1]
                for token in condition:
                    if token[0] == 'IDENTIFIER':
                        self.lookup(token[1])
            elif token_type == 'ASSIGN':
                var_name = statement[1]
                self.lookup(var_name)
                expression = statement[2]
                for token in expression:
                    if token[0] == 'IDENTIFIER':
                        self.lookup(token[1])

class MiniParParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0
        self.current_token = self.tokens[self.current_token_index] if tokens else None
        self.symbol_table = SymbolTable()

    def advance(self):
        """Avança para o próximo token."""
        self.current_token_index += 1
        if self.current_token_index < len(self.tokens):
            self.current_token = self.tokens[self.current_token_index]
        else:
            self.current_token = None

    def parse(self):
        """Inicia a análise do programa."""
        self.programa_minipar()

    def programa_minipar(self):
        self.bloco_stmt()
        self.symbol_table.check(self.tokens)

    def bloco_stmt(self):
        if self.current_token[0] == 'SEQ':
            self.bloco_SEQ()
        elif self.current_token[0] == 'PAR':
            self.bloco_PAR()
        else:
            raise SyntaxError("Esperado 'SEQ' ou 'PAR'.")

    def bloco_SEQ(self):
        self.match('SEQ')
        self.stmts()

    def bloco_PAR(self):
        self.match('PAR')
        self.stmts()

    def stmts(self):
        while self.current_token:
            if self.current_token[0] == 'IDENTIFIER':
                self.atribuicao()
            elif self.current_token[0] == 'IF':
                self.if_stmt()
            elif self.current_token[0] == 'WHILE':
                self.while_stmt()
            elif self.current_token[0] == 'C_CHANNEL':
                self.canal_com()
            else:
                break

    def atribuicao(self):
        var_name = self.current_token[1]
        self.match('IDENTIFIER')
        self.match('ASSIGN')
        self.expr()
        self.symbol_table.define(var_name, "int")  # Supondo tipo padrão 'int'

    def if_stmt(self):
        self.match('IF')
        self.match('LPAREN')
        self.bool_expr()
        self.match('RPAREN')
        self.stmts()
        if self.current_token and self.current_token[0] == 'ELSE':
            self.match('ELSE')
            self.stmts()

    def while_stmt(self):
        self.match('WHILE')
        self.match('LPAREN')
        self.bool_expr()
        self.match('RPAREN')
        self.stmts()

    def canal_com(self):
        self.match('C_CHANNEL')
        channel_name = self.current_token[1]
        self.match('IDENTIFIER')  # Nome do canal
        sender = self.current_token[1]
        self.match('IDENTIFIER')  # Emissor
        receiver = self.current_token[1]
        self.match('IDENTIFIER')  # Receptor
        self.symbol_table.define(channel_name, "channel")  # Define canal

    def bool_expr(self):
        self.match('BOOL')

    def expr(self):
        self.match('IDENTIFIER')
        while self.current_token and self.current_token[0] in ('+', '-', '*', '/'):
            self.match(self.current_token[0])
            self.match('IDENTIFIER')

    def match(self, token_type):
        if self.current_token and self.current_token[0] == token_type:
            self.advance()
        else:
            raise SyntaxError(f"Esperado '{token_type}', mas encontrado '{self.current_token}'.")

