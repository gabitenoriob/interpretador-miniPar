from analisadorLexico import tokenize

class SymbolTable:
    def __init__(self):
        self.symbols = {}

    def define(self, name, var_type):
        if name in self.symbols:
            raise Exception(f"Erro: A variável '{name}' já foi declarada.")
        self.symbols[name] = var_type

    def lookup(self, name):
        if name not in self.symbols:
            raise Exception(f"Erro: A variável '{name}' não foi declarada.")
        return self.symbols[name]

    def check(self, program):
        """Verifica a semântica do programa com base nos tokens."""
        for statement in program:
            token_type = statement[0]
            if token_type == 'IDENTIFIER':
                var_name = statement[1]
                self.lookup(var_name)  # Verifica se a variável foi declarada
            elif token_type in {'SEND', 'RECEIVE'}:
                # Verifica o uso correto de operações de comunicação
                var_name = statement[1]
                self.lookup(var_name)  # Verifica se o canal/variável foi declarado
            elif token_type in {'IF', 'WHILE'}:
                # Verifica se a condição contém variáveis declaradas
                condition = statement[1]  # Supondo que a condição seja passada como lista de tokens
                for token in condition:
                    if token[0] == 'IDENTIFIER':
                        self.lookup(token[1])  # Verifica variáveis na condição
            elif token_type == 'ASSIGN':
                var_name = statement[1]
                self.lookup(var_name)  # Verifica se a variável existe para a atribuição
                expression = statement[2]  # Supondo que a expressão seja uma lista de tokens
                for token in expression:
                    if token[0] == 'IDENTIFIER':
                        self.lookup(token[1])  # Verifica variáveis na expressão
            # Adiciona outros casos de tokens conforme necessário



class MiniParParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0
        self.current_token = self.tokens[self.current_token_index] if tokens else None
        self.symbol_table = SymbolTable()  # Inicializa a tabela de símbolos

    # Função para avançar para o próximo token
    def advance(self):
        self.current_token_index += 1
        if self.current_token_index < len(self.tokens):
            self.current_token = self.tokens[self.current_token_index]
        else:
            self.current_token = None

    def parse(self):
        """Inicia a análise do programa MiniPar."""
        self.programa_minipar()

    def programa_minipar(self):
        """Verifica a produção 'programa_minipar'."""
        self.bloco_stmt()
        # Após a análise sintática, verificamos a semântica
        self.symbol_table.check(self.tokens)  # Verificação semântica

    def bloco_stmt(self):
        """Verifica a produção 'bloco_stmt'."""
        if self.current_token[0] == 'SEQ':
            self.bloco_SEQ()
        elif self.current_token[0] == 'PAR':
            self.bloco_PAR()
        else:
            raise SyntaxError("Esperado 'SEQ' ou 'PAR'.")

    def bloco_SEQ(self):
        """Verifica a produção 'bloco_SEQ'."""
        self.match('SEQ')
        self.stmts()

    def bloco_PAR(self):
        """Verifica a produção 'bloco_PAR'."""
        self.match('PAR')
        self.stmts()

    def stmts(self):
        """Verifica a produção 'stmts'."""
        while self.current_token:
            if self.current_token[0] == 'IDENTIFIER':
                self.atribuição()
            elif self.current_token[0] == 'IF':
                self.if_stmt()
            elif self.current_token[0] == 'WHILE':
                self.while_stmt()
            else:
                break

    def atribuição(self):
        """Verifica a produção 'atribuição'."""
        var_name = self.current_token[1]
        self.match('IDENTIFIER')
        self.match('ASSIGN')
        self.expr()
        self.symbol_table.define(var_name, "int")  # Define o tipo como 'int' para a atribuição

    def if_stmt(self):
        """Verifica a produção 'if'."""
        self.match('IF')
        self.match('LPAREN')
        self.bool_expr()
        self.match('RPAREN')
        self.stmts()
        if self.current_token and self.current_token[0] == 'ELSE':
            self.match('ELSE')
            self.stmts()

    def while_stmt(self):
        """Verifica a produção 'while'."""
        self.match('WHILE')
        self.match('LPAREN')
        self.bool_expr()
        self.match('RPAREN')
        self.stmts()

    def bool_expr(self):
        """Verifica a expressão booleana."""
        self.match('BOOL')

    def expr(self):
        """Verifica a produção 'expr'."""
        self.match('IDENTIFIER')  # Exemplo de simplificação
        while self.current_token and self.current_token[0] in ('+', '-', '*', '/'):
            self.match(self.current_token[0])  # Avança no operador
            self.match('IDENTIFIER')  # Avança no operando

    def match(self, token_type):
        """Verifica se o próximo token é do tipo esperado."""
        if self.current_token and self.current_token[0] == token_type:
            self.advance()
        else:
            raise SyntaxError(f"Esperado '{token_type}', mas encontrado '{self.current_token}'.")



