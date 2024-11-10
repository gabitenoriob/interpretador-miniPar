from analisadorLexico import tokenize
from analisadorSemantico import SymbolTable



class MiniParParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0
        self.current_token = self.tokens[self.current_token_index] if tokens else None

    def advance(self):
        """Avança para o próximo token."""
        self.current_token_index += 1
        if self.current_token_index < len(self.tokens):
            self.current_token = self.tokens[self.current_token_index]
        else:
            self.current_token = None

    def parse(self):
        """Inicia a análise do programa MiniPar."""
        self.programa_minipar()
        return self.tokens  # Retorna a estrutura ou resultado da análise

    def programa_minipar(self):
        """Verifica a produção 'programa_minipar'."""
        # Trata declarações de canal antes do bloco principal
        while self.current_token and self.current_token[0] == 'C_CHANNEL':
            self.declaracao_canal()
        
        # Continua com o bloco de instruções principal
        self.bloco_stmt()

    def declaracao_canal(self):
        """Verifica a produção de declaração de canal."""
        self.match('C_CHANNEL')
        while self.current_token and self.current_token[0] == 'IDENTIFIER':
            self.match('IDENTIFIER')


    def bloco_stmt(self):
        """Verifica a produção 'bloco_stmt'."""
        print(f"Token atual: {self.current_token}")  # Verifique o token no momento da análise
        if self.current_token and self.current_token[0] == 'SEQ':
            self.bloco_SEQ()
        elif self.current_token and self.current_token[0] == 'PAR':
            self.bloco_PAR()
        else:
            raise SyntaxError(f"Esperado 'SEQ' ou 'PAR', mas encontrado '{self.current_token}'.")


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
                # Verifica se é uma chamada de função ou uma atribuição
                next_index = self.current_token_index + 1
                if next_index < len(self.tokens) and self.tokens[next_index][0] == 'LPAREN':
                    self.func_call()  # Trata chamada de função
                else:
                    self.atribuição()  # Trata atribuição
            elif self.current_token[0] == 'IF':
                self.if_stmt()
            elif self.current_token[0] == 'WHILE':
                self.while_stmt()
            else:
                break

    def func_call(self):
        """Verifica a produção de chamada de função."""
        self.match('IDENTIFIER')
        self.match('LPAREN')
        # Lida com argumentos de função, se houver
        while self.current_token and self.current_token[0] != 'RPAREN':
            self.expr()  # Processa argumentos de forma recursiva
            if self.current_token and self.current_token[0] == 'COMMA':
                self.match('COMMA')
        self.match('RPAREN')  # Finaliza a chamada de função


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
        if self.current_token[0] in ['IDENTIFIER', 'STRING']:
            self.match(self.current_token[0])
            if self.current_token[1] == '=':
                self.match('ASSIGN')
                if self.current_token[0] in ['IDENTIFIER', 'STRING']:
                    self.match(self.current_token[0])
                    return True
            else:
                raise SyntaxError("Operador de comparação esperado ('=').")
        else:
            raise SyntaxError("Expressão booleana inválida.")



    def atribuição(self):
        """Verifica a produção 'atribuição'."""
        self.match('IDENTIFIER')
        self.match('ASSIGN')
        self.expr()  # Permite chamadas de função ou expressões completas

    def expr(self):
        """Verifica a produção 'expr'."""
        if self.current_token[0] == 'IDENTIFIER':
            self.match('IDENTIFIER')
            if self.current_token and self.current_token[0] == 'LPAREN':
                self.match('LPAREN')
                # Lida com argumentos de função, se houver
                while self.current_token and self.current_token[0] != 'RPAREN':
                    self.expr()  # Processa argumentos de forma recursiva
                    if self.current_token and self.current_token[0] == 'COMMA':
                        self.match('COMMA')
                self.match('RPAREN')  # Finaliza a chamada de função
        elif self.current_token[0] == 'STRING':
            # Lida com uma string de solicitação de entrada do usuário
            print(self.current_token[1])  # Exibe a mensagem no terminal
            resposta = input()  # Captura a resposta do usuário
            print(f"Resposta: {resposta}")  # Você pode fazer algo com a resposta depois
            self.advance()  # Avança para o próximo token
        else:
            raise SyntaxError(f"Esperado 'IDENTIFIER' ou expressão, mas encontrado '{self.current_token}'.")


    def match(self, token_type):
        """Verifica se o próximo token é do tipo esperado."""
        if self.current_token and self.current_token[0] == token_type:
            self.advance()
        else:
            raise SyntaxError(f"Esperado '{token_type}', mas encontrado '{self.current_token}'.")
