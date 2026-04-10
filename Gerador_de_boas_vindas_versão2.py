def gerar_mensagem_boas_vindas(nome, idade):
    return f"Olá {nome}, você tem {idade} anos. Seja bem-vindo!"

nome = input("Digite seu nome: ")
idade = int(input("Digite sua idade: "))

mensagem = gerar_mensagem_boas_vindas(nome, idade)

print(mensagem)