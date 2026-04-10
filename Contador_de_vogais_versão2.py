def contar_vogais(texto):
    texto = texto.lower()
    contador = 0

    for letra in texto:
        if letra in "aeiou":
            contador += 1

    return contador

texto = input("Digite uma palavra ou frase: ")
resultado = contar_vogais(texto)

print("Total de vogais:", resultado)