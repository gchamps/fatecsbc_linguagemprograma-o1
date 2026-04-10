senha = input("Digite uma senha: ")

while len(senha) < 8:
    print("Senha inválida! Precisa ter pelo menos 8 caracteres.")
    senha = input("Digite novamente: ")

print("Senha válida!")