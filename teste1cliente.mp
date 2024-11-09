# Programa cliente (computador_1) de uma calculadora aritmética simples

# Declaração do canal de comunicação
c_channel calculadora computador_1 computador_2

SEQ
    # Apresenta as opções de operação aritmética
    print("Escolha uma operacao aritmetica: +, -, *, /")

    # Lê a operação aritmética desejada
    operacao = sys.stdin.readline()

    # Lê o primeiro operando
    print("Digite o primeiro valor:")
    valor1 = sys.stdin.readline()

    # Lê o segundo operando
    print("Digite o segundo valor:")
    valor2 = sys.stdin.readline()

    # Envia a solicitação para o servidor (computador_2)
    calculadora.send(operacao, valor1, valor2, resultado)

    # Imprime o resultado do cálculo
    print("Resultado da operacao: ", resultado)
