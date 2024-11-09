# Teste de execução paralela para cálculo do fatorial e série de Fibonacci

PAR
    # Cálculo do fatorial de um número (thread 1)
    Int n = 5
    Int fatorial = 1
    while (n > 1)
        fatorial = fatorial * n
        n = n - 1
    print("Fatorial calculado: ", fatorial)

    # Cálculo da série de Fibonacci (thread 2)
    Int fib1 = 0
    Int fib2 = 1
    Int proximo
    Int contador = 0
    Int limite = 10  # número de termos a serem calculados

    while (contador < limite)
        print("Termo ", contador + 1, ": ", fib1)
        proximo = fib1 + fib2
        fib1 = fib2
        fib2 = proximo
        contador = contador + 1

    # As threads serão executadas simultaneamente
