def calcular_area_retangulo(base, altura):
    return base * altura

base = float(input("Digite a base: "))
altura = float(input("Digite a altura: "))

area = calcular_area_retangulo(base, altura)

print("Área:", area)