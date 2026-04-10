def validar_senha(senha):
    return len(senha) >= 8

senha = input("Digite uma senha: ")

while not validar_senha(senha):
    print("Senha inválida! Precisa ter pelo menos 8 caracteres.")
    senha = input("Digite novamente: ")

print("Senha válida!")