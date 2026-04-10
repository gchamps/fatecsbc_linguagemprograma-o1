valor = float(input("Digite o valor do produto: "))
desconto = float(input("Digite o percentual de desconto: "))

desconto_valor = valor * (desconto / 100)
valor_final = valor - desconto_valor

print("Valor final:", valor_final)