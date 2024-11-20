SEQ{
    # Recebe a solicitação de operação aritmética
    calculadora.receive(operacao, valor1, valor2, resultado)

    # Executa o cálculo com base na operação solicitada
    if (operacao = "+")
        resultado = valor1 + valor2
    else if (operacao = "-")
        resultado = valor1 - valor2
    else if (operacao = "*")
        resultado = valor1 * valor2
    else if (operacao = "/")
        resultado = valor1 / valor2
    else
        Output("Operação inválida")

    # Retorna o resultado para o cliente (computador_1)
    calculadora.send(operacao, valor1, valor2, resultado)
}
