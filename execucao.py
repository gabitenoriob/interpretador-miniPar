import analisadorLexico
import analisadorSemantico
import analisadorSintatico
import socket
import threading

has_error = False
symbol_table = {}
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
        var_value = input("Digite um valor para {}: ".format(var_name))
        symbol_table[var_name] = var_value

    elif stmt[0] == 'OUTPUT':
        if isinstance(stmt[1], tuple):
            for v in stmt[1]:
                execute_output(v)
        else:
            execute_output(stmt[1])

    elif stmt[0] == '=':
        var_name = stmt[1]
        value = stmt[2]
        if value == "INPUT":
            value = execute_stmt((value, var_name))     
        else:
            value = evaluate_expr(value)
            symbol_table[var_name] = value

    elif stmt[0] == "C_CHANNEL":
        channels[stmt[1]] = (stmt[2], stmt[3])

    elif not isinstance(stmt[0], tuple) and stmt[0] in channels:
        if stmt[1] == 'SEND':
            channel_name = stmt[0]
            channel = channels.get(channel_name)
            if channel:
                if len(stmt) == 6:
                    _, _, operation, value1, value2, result = stmt
                    send_data(channel[1], 9999, f"{symbol_table[operation]},{symbol_table[value1]},{symbol_table[value2]},{result}")
                elif len(stmt) == 3:
                    send_data(channel[1], 9998, f"{symbol_table[stmt[2]]}")
        elif stmt[1] == "RECEIVE":
            channel_name = stmt[0]
            channel = channels.get(channel_name)
            if channel:
                if len(stmt) == 6:
                    stringRec = receive_data(channel[1], 9999)
                    operation, value1, value2, result = stringRec.split(",")
                    symbol_table[stmt[2]] = operation
                    symbol_table[stmt[3]] = int(value1)
                    symbol_table[stmt[4]] = int(value2)
                    symbol_table[stmt[5]] = result
                elif len(stmt) == 3:
                    stringRec = receive_data(channel[1], 9998)
                    symbol_table[stmt[2]] = stringRec

    elif isinstance(stmt, tuple):
        for s in stmt:
            execute_stmt(s)

def execute_output(v):
    var_name = v
    var_value = symbol_table.get(var_name, None)
    if var_value is not None:
        formatted_output = var_value
        print(formatted_output, end='')
    else:
        formatted_output = var_name.replace("\\n", "\n")
        print(formatted_output, end='')

def execute_bool(expr):
    if isinstance(expr, tuple):
        op, left, right = expr
        left = symbol_table.get(left, 0)
        right = symbol_table.get(right, 0)
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

def evaluate_expr(expr):
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
        return symbol_table.get(expr, expr)

def send_data(host, port, data):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((host, port))
        sock.sendall(data.encode())
    finally:
        sock.close()

def receive_data(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.bind((host, port))
        server_socket.listen(5)
        while True:
            client_socket, address = server_socket.accept()
            data = client_socket.recv(1024)
            if not data:
                break
            return data.decode()
            client_socket.close()
    finally:
        server_socket.close()

def run_minipar(file_path):
    with open(file_path, 'r') as file:
        source_code = file.read()
    
    # Analisador Léxico
    tokens = analisadorLexico.tokenize(source_code)
    print("Tokens gerados:", tokens)

    # Analisador Sintático
    parsed_code = analisadorSintatico.parse(tokens)
    print("Código parseado:", parsed_code)

    # Analisador Semântico
    if analisadorSemantico.check(parsed_code):
        print("Análise semântica bem-sucedida.")
        # Executor de Instruções
        execute_stmt(parsed_code)
    else:
        print("Erros na análise semântica.")

if __name__ == "__main__":
    run_minipar("teste1.mp")
