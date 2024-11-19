import argparse
import os
import sys
import threading
import socket
from analisadorLexico import tokens, tokenize
import analisadorLexico
from analisadorSintatico import parser
from analisadorSemantico import SymbolTable
import analisadorSintatico

symbol_table = SymbolTable()
channels = {}


# Funções de execução para cada tipo de instrução
def execute_stmt(stmt):
    if stmt[0] == 'SEQ':
        for s in stmt[1]:
            execute_stmt(s)

    elif stmt[0] == 'PAR':
        threads = []
        for s in stmt[1]:
            thread = threading.Thread(target=execute_stmt, args=(s,))
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()

    elif stmt[0] == 'IF':
        if execute_bool(stmt[1]):
            for s in stmt[2]:
                execute_stmt(s)

    elif stmt[0] == 'WHILE':
        while execute_bool(stmt[1]):
            for s in stmt[2]:
                execute_stmt(s)

    elif stmt[0] == 'INPUT':
        var_name = stmt[1]
        var_value = input(f"Digite um valor para {var_name}: ")
        symbol_table.define(var_name, "int")  # Define como int para simplificar
        symbol_table.symbols[var_name] = int(var_value)

    elif stmt[0] == 'OUTPUT':
        for v in stmt[1]:
            execute_output(v)

    elif stmt[0] == '=':
        var_name = stmt[1]
        value = evaluate_expr(stmt[2])
        symbol_table.symbols[var_name] = value

    elif stmt[0] == 'C_CHANNEL':
        channels[stmt[1]] = (stmt[2], stmt[3])

    elif stmt[0] in channels:
        if stmt[1] == 'SEND':
            send_data(channels[stmt[0]][1], 9999, str(evaluate_expr(stmt[2])))

        elif stmt[1] == 'RECEIVE':
            received_value = receive_data(channels[stmt[0]][1], 9999)
            symbol_table.symbols[stmt[2]] = int(received_value)


def execute_output(v):
    var_name = v
    var_value = symbol_table.get(var_name, None)
    if var_value is not None:           #Se está na tabela de símbolos...
        formatted_output = var_value
        print(formatted_output, end='')     #end='' garante que não pule linha automaticamente
    else:
        formatted_output = var_name.replace("\\n", "\n")    #substitui qualquer \n na string pela quebra de linha real
        print(formatted_output, end='')


def execute_bool(expr):
    op, left, right = expr
    left_val = evaluate_expr(left)
    right_val = evaluate_expr(right)
    return eval(f"{left_val} {op} {right_val}")


def execute_bool(expr):
    if isinstance(expr, tuple):

        op, left, right = expr

        if left in symbol_table:
            left = symbol_table.get(left, 0)  # Obter o valor da variável ou 0 se não existir
        if right in symbol_table:
            right = symbol_table.get(right, 0)  # Obter o valor da variável ou 0 se não existir
            
        if op == '<':
            return evaluate_expr(left) < evaluate_expr(right)
        elif op == '>':
            return evaluate_expr(left) > evaluate_expr(right)
        elif op == '<=':
            return evaluate_expr(left) <= evaluate_expr(right)
        elif op == '>=':
            return evaluate_expr(left) >= evaluate_expr(right)
        elif op == '==':
            return evaluate_expr(left) == evaluate_expr(right)
        elif op == '!=':
            return evaluate_expr(left) != evaluate_expr(right)
    return False

#Avalia as expressões aritméticas
def evaluate_expr(expr):
    #se for um inteiro ou sinal de uma operação aritmética simples não precisa calcular nada, então apenas retorna o próprio valor
    if isinstance(expr, int) or expr in {'-', '+', '*', '/'}:
        return expr
    elif isinstance(expr, tuple):
        op, left, right = expr
        if op == '+':
            return evaluate_expr(left) + evaluate_expr(right)
        elif op == '-':
            return evaluate_expr(left) - evaluate_expr(right)
        elif op == '*':
            return evaluate_expr(left) * evaluate_expr(right)
        elif op == '/':
            return evaluate_expr(left) / evaluate_expr(right)
        elif any(op == x for x in ['<', '>', '<=', '>=', '==', '!=']):
            return execute_bool(expr)
    elif isinstance(expr, str):
        return symbol_table.get(expr, expr)  # Retorna o valor da variável na tabela de simbolos, se não tiver retorna a propria string


def send_data(host, port, data):
    #print(f"host: {host} \nport: {port} \ndata: {data}")
    # Cria um socket TCP
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Conecta ao host e porta especificados
        sock.connect((host, port))
        # Envia os dados
        sock.sendall(data.encode())
    finally:
        # Fecha o socket
        sock.close()
        #print("conexão cliente fechada")


def receive_data(host, port):
    #print(f"host: {host} port: {port}")
    # Cria um socket TCP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Associa o socket ao host e à porta especificados
        server_socket.bind((host, port))
        # Escuta por conexões
        server_socket.listen(5)
        #print("Aguardando conexão...")
        
        while True:
            # Aceita a conexão
            client_socket, address = server_socket.accept()
            #print(f"Conexão estabelecida com {address}")
            
            # Recebe os dados
            data = client_socket.recv(1024)
            if not data:
                break
            
            # Retorna a string recebida
            return data.decode()
            # Fecha o socket do cliente
            client_socket.close()
    finally:
        # Fecha o socket do servidor
        server_socket.close()


def run_minipar(file_path):
    with open(file_path, 'r') as file:
        source_code = file.read()

    # Analisador Léxico
    tokens = tokenize(source_code)
    print("Tokens gerados:", tokens)

    # Analisador Sintático
    # Aqui, o parser.parse deve ser chamado no código-fonte já tokenizado
    try:
        ast = parser.parse(source_code)  # Gera a AST (árvore sintática abstrata)
        print("Árvore Sintática Gerada:", ast)
    except Exception as e:
        print("Erro na análise sintática:", e)
        return

    # Análise Semântica
    try:
        # Se a análise semântica precisar da AST, passe ela ao invés de tokens
        symbol_table.check(ast)  # Usando a AST gerada para a verificação semântica
        print("Análise semântica bem-sucedida.")
    except Exception as e:
        print("Erro na análise semântica:", e)
        return

    # Executor de Instruções
    try:
        execute_stmt(ast)  # Executando as instruções com base na AST
        print("Execução bem-sucedida.")
    except Exception as e:
        print("Erro na execução:", e)
        return




def client_thread(file_path):
    run_minipar(file_path)


def server_thread():
    host = 'localhost'
    port = 9999
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen(5)
        print(f"Servidor rodando em {host}:{port}...")
        while True:
            client_socket, address = server_socket.accept()
            print(f"Conexão com {address}")
            client_socket.close()


# Testar o interpretador MiniPar
        
def read_program_from_file(file_path):
    with open(file_path, 'r') as file:
        program = file.read()
    return program

def main():
    #Verifica se comando no terminal numero de argumentos diferente do esperado (2)
    if len(sys.argv) != 2:
        print("Uso: python main.py <nome_do_program.mp> ou minipar <nome_do_programa>")
        sys.exit(1)

    program_file = sys.argv[1]

    # Verifica se o programa é inexistente
    if not os.path.exists(program_file):
        print(f"Erro: O arquivo '{program_file}' não foi encontrado.")
        sys.exit(1)
    
    # Ler programa
    entrada = read_program_from_file(program_file)
    
    lexer = analisadorLexico.lexer
    result = analisadorSintatico.parser.parse(entrada, lexer=lexer)
    
    if result:
        if not exec.has_error:
            exec.execute_stmt(result)
        else:
            pass

if __name__ == "__main__":
    main()
