import analisadorSintatico as ps
import analisadorLexico as lexic
import interpretador as exec
import sys
import os
#
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
    
    lexer = lexic.lexer
    result = ps.parser.parse(entrada, lexer=lexer)
    
    if result:
        if not exec.has_error:
            exec.execute_stmt(result)
        else:
            pass

if __name__ == "__main__":
    main()