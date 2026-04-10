def verificar_paridade(n):
    if n % 2 == 0:
        print("Par")
    else:
        print("Ímpar")

numero = int(input("Digite um número: "))
verificar_paridade(numero)