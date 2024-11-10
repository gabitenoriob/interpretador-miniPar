# Programa cliente (computador_1) de uma calculadora aritmética simples

# Declaração do canal de comunicação
c_channel calculadora computador_1 computador_2

SEQ
    # Apresenta as opções de operação aritmética
    Output("Escolha uma operacao aritmetica: +, -, *, /")

    # Lê a operação aritmética desejada
    operacao = Input()

    # Lê o primeiro operando
    Output("Digite o primeiro valor:")
    valor1 = Input()

    # Lê o segundo operando
    Output("Digite o segundo valor:")
    valor2 = Input()

    # Envia a solicitação para o servidor (computador_2)
    calculadora.send(operacao, valor1, valor2, resultado)

    # Imprime o resultado do cálculo
    Output("Resultado da operacao: ", resultado)
