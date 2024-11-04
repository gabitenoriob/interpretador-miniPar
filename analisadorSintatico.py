from analisadorLexico import tokenize

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

    def programa_minipar(self):
        """Verifica a produção 'programa_minipar'."""
        self.bloco_stmt()

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
        self.match('IDENTIFIER')
        self.match('ASSIGN')
        self.expr()

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
            self.match(self.current_token[0])  # avança no operador
            self.match('IDENTIFIER')  # avança no operando

    def match(self, token_type):
        """Verifica se o próximo token é do tipo esperado."""
        if self.current_token and self.current_token[0] == token_type:
            self.advance()
        else:
            raise SyntaxError(f"Esperado '{token_type}', mas encontrado '{self.current_token}'.")

def main():
    code = """
    SEQ {
        x = 5;
        if (Bool) {
            send x to c_channel;
        } else {
            receive y from c_channel;
        }
    }
    """
    
    try:
        tokens = tokenize(code)
        parser = MiniParParser(tokens)
        parser.parse()
        print("Análise sintática bem-sucedida!")
    except (ValueError, SyntaxError) as e:
        print(e)

if __name__ == '__main__':
    main()