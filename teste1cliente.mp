# Programa cliente (computador_1) de uma calculadora aritmética simples

SEQ
    Output("Escolha uma operacao aritmetica: +, -, *, /")
    operacao = Input()

    Output("Digite o primeiro valor:")
    valor1 = Input()

    Output("Digite o segundo valor:")
    valor2 = Input()

    # Envia a solicitação para o servidor (computador_2)
    calculadora.send(operacao, valor1, valor2, resultado)

    # Aguardar e receber a resposta do servidor
    calculadora.receive(operacao, valor1, valor2, resultado)

    # Imprime o resultado do cálculo
    Output("Resultado da operacao: ", resultado)
