def classificar_nota(nota):
    if nota >= 90:
        return "A"
    elif nota >= 80:
        return "B"
    elif nota >= 70:
        return "C"
    elif nota >= 60:
        return "D"
    else:
        return "E"

nota = float(input("Digite a nota: "))
resultado = classificar_nota(nota)

print("Classificação:", resultado)