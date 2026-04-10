texto = input("Digite uma palavra ou frase: ").lower()

contador = 0

for letra in texto:
    if letra in "aeiou":
        contador += 1

print("Total de vogais:", contador)