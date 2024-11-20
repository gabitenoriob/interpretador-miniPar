from analisadorLexico import tokens 
#
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
                self.lookup(var_name)  # Verifica a variável
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
        self.program = []

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
        """Inicia a análise do programa completo."""
        self.bloco_stmt()
        self.symbol_table.check(self.program)

    def bloco_stmt(self):
        """Analisa um bloco de sentenças (SEQ ou PAR)."""
        if self.current_token[0] == 'SEQ':
            self.bloco_SEQ()
        elif self.current_token[0] == 'PAR':
            self.bloco_PAR()
        else:
            raise SyntaxError("Esperado 'SEQ' ou 'PAR'.")

    def bloco_SEQ(self):
        """Analisa um bloco SEQ."""
        self.match('SEQ')
        self.stmts()

    def bloco_PAR(self):
        """Analisa um bloco PAR."""
        self.match('PAR')
        self.stmts()

    def stmts(self):
        """Analisa uma lista de sentenças."""
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
        """Analisa uma sentença de atribuição."""
        var_name = self.current_token[1]
        self.match('IDENTIFIER')
        self.match('ASSIGN')
        expr_result = self.expr()
        self.symbol_table.define(var_name, "int")  # Supondo tipo 'int'
        self.program.append(('ASSIGN', var_name, expr_result))  # Adiciona à lista de sentenças

    def if_stmt(self):
        """Analisa uma sentença de IF."""
        self.match('IF')
        self.match('LPAREN')
        condition = self.bool_expr()
        self.match('RPAREN')
        self.stmts()
        if self.current_token and self.current_token[0] == 'ELSE':
            self.match('ELSE')
            self.stmts()
        self.program.append(('IF', condition))

    def while_stmt(self):
        """Analisa uma sentença de WHILE."""
        self.match('WHILE')
        self.match('LPAREN')
        condition = self.bool_expr()
        self.match('RPAREN')
        self.stmts()
        self.program.append(('WHILE', condition))

    def canal_com(self):
        """Analisa uma comunicação de canal."""
        self.match('C_CHANNEL')
        channel_name = self.current_token[1]
        self.match('IDENTIFIER')  # Nome do canal
        sender = self.current_token[1]
        self.match('IDENTIFIER')  # Emissor
        receiver = self.current_token[1]
        self.match('IDENTIFIER')  # Receptor
        self.symbol_table.define(channel_name, "channel")  # Define canal
        self.program.append(('C_CHANNEL', channel_name, sender, receiver))

    def bool_expr(self):
        """Analisa expressões booleanas."""
        self.match('BOOL')
        return self.current_token[1]  # Retorna o valor da expressão booleana

    def expr(self):
        """Analisa uma expressão (operadores aritméticos)."""
        left = self.match('IDENTIFIER')  # Inicia com um identificador
        while self.current_token and self.current_token[0] in ('+', '-', '*', '/'):
            op = self.current_token[0]
            self.advance()  # Avança para o próximo token (operador)
            right = self.match('IDENTIFIER')  # Próximo identificador
            left = (op, left, right)
        return left

    def match(self, token_type):
        """Compara o token atual com o esperado e avança."""
        if self.current_token and self.current_token[0] == token_type:
            token = self.current_token
            self.advance()
            return token[1]  # Retorna o valor do token
        else:
            raise SyntaxError(f"Esperado '{token_type}', mas encontrado '{self.current_token}'.")
