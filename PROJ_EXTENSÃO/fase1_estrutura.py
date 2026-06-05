"""
=============================================================================
PROJETO DE EXTENSÃO – LINGUAGEM DE PROGRAMAÇÃO I
Disciplina: Linguagem de Programação I | Curso: ADS | FATEC
Organização Parceira: PetShop AmigoPet Ltda.
Fase 1: Estrutura Inicial dos Dados e Cálculo Principal do Negócio
=============================================================================
Descrição:
    Este módulo define a estrutura de dados fundamental do sistema de
    gerenciamento de serviços do PetShop AmigoPet. Apresenta variáveis,
    constantes, tipos de dados, dados de exemplo e o cálculo principal
    do negócio (precificação com desconto e impostos).

Autor: Projeto Extensão – Turma ADS 2025
Data: 2025
=============================================================================
"""

# ============================================================
# SEÇÃO 1: CONSTANTES DO SISTEMA
# (Valores fixos que não se alteram durante a execução)
# ============================================================

# Alíquota de desconto progressiva por fidelidade (float: permite casas decimais)
DESCONTO_CLIENTE_FIDELIDADE = 0.10       # 10% de desconto para clientes fidelizados
DESCONTO_SERVICO_COMBO     = 0.15        # 15% de desconto para combos de serviço

# Imposto sobre serviço (ISS) conforme legislação municipal (float)
ALIQUOTA_ISS               = 0.05        # 5% de ISS sobre o valor do serviço

# Preços-base dos serviços (float: valores monetários com centavos)
PRECO_BANHO_PEQUENO        = 45.00       # R$ 45,00 – porte pequeno
PRECO_BANHO_MEDIO          = 65.00       # R$ 65,00 – porte médio
PRECO_BANHO_GRANDE         = 90.00       # R$ 90,00 – porte grande
PRECO_TOSA_SIMPLES         = 55.00       # R$ 55,00 – tosa higiênica
PRECO_TOSA_COMPLETA        = 85.00       # R$ 85,00 – tosa completa
PRECO_CONSULTA_VETERINARIA = 150.00      # R$ 150,00 – consulta veterinária
PRECO_VACINA               = 80.00       # R$ 80,00 – aplicação de vacina
PRECO_HOSPEDAGEM_DIARIA    = 120.00      # R$ 120,00 – diária de hospedagem

# Porte dos animais (str: categorias textuais)
PORTE_PEQUENO              = "Pequeno"
PORTE_MEDIO                = "Médio"
PORTE_GRANDE               = "Grande"

# Status possíveis de um agendamento (str: estado do processo)
STATUS_AGENDADO            = "Agendado"
STATUS_EM_ANDAMENTO        = "Em Andamento"
STATUS_CONCLUIDO           = "Concluído"
STATUS_CANCELADO           = "Cancelado"

# Limite de alertas de lotação da agenda (int: número inteiro de slots)
LIMITE_AGENDA_DIARIA       = 20          # máximo de 20 atendimentos por dia

# ============================================================
# SEÇÃO 2: DADOS DE EXEMPLO (simulam registros reais)
# ============================================================

# Dicionário de cliente (dict: estrutura chave-valor flexível para atributos)
cliente_exemplo = {
    "id"          : 1,                     # int  – identificador único
    "nome"        : "Maria Oliveira",      # str  – nome completo
    "cpf"         : "123.456.789-00",      # str  – CPF com máscara
    "telefone"    : "(11) 98765-4321",     # str  – número de contato
    "email"       : "maria@email.com",     # str  – endereço de e-mail
    "fidelidade"  : True,                  # bool – cliente cadastrado no programa
    "pets"        : ["Thor", "Luna"],      # list – nomes dos pets do cliente
}

# Dicionário de pet (dict: agrupa todos os atributos do animal)
pet_exemplo = {
    "id"          : 1,                     # int  – identificador único
    "nome"        : "Thor",                # str  – nome do animal
    "especie"     : "Cão",                 # str  – espécie (Cão, Gato, etc.)
    "raca"        : "Golden Retriever",    # str  – raça
    "porte"       : PORTE_GRANDE,          # str  – constante de porte
    "idade"       : 3,                     # int  – idade em anos
    "peso_kg"     : 28.5,                  # float– peso em quilogramas
    "id_cliente"  : 1,                     # int  – referência ao proprietário
}

# Dicionário de agendamento (dict: registra o serviço agendado)
agendamento_exemplo = {
    "id"          : 1,                     # int  – identificador único
    "id_cliente"  : 1,                     # int  – referência ao cliente
    "id_pet"      : 1,                     # int  – referência ao pet
    "servico"     : "Banho e Tosa Completa", # str – descrição do serviço
    "data"        : "2025-08-15",          # str  – data no formato ISO 8601
    "hora"        : "09:00",               # str  – horário de atendimento
    "status"      : STATUS_AGENDADO,       # str  – estado atual
    "valor_bruto" : 0.0,                   # float– valor antes de descontos/impostos
    "valor_final" : 0.0,                   # float– valor após cálculos
    "observacoes" : "Pet sensível a ruídos", # str – informações adicionais
}

# ============================================================
# SEÇÃO 3: CÁLCULO PRINCIPAL DO NEGÓCIO
# Precificação com desconto por fidelidade e acréscimo de ISS
# ============================================================

def calcular_valor_servico(preco_base: float, fidelidade: bool,
                            combo: bool = False) -> dict:
    """
    Calcula o valor final de um serviço considerando descontos e impostos.

    Parâmetros:
        preco_base (float) : Valor bruto do serviço sem qualquer ajuste.
        fidelidade (bool)  : True se o cliente está no programa de fidelidade.
        combo      (bool)  : True se o cliente contratou um combo de serviços.

    Retorno:
        dict : Dicionário com breakdown financeiro detalhado.

    Regras de Negócio:
        RN-01: Desconto de fidelidade (10%) não se acumula com desconto de combo.
        RN-02: O maior desconto aplicável prevalece (critério mais vantajoso ao cliente).
        RN-03: ISS de 5% é sempre acrescido sobre o valor com desconto.
        RN-04: Valores monetários são arredondados para 2 casas decimais.
    """

    # Passo 1 – Determinar o percentual de desconto aplicável (RN-01 e RN-02)
    percentual_desconto = 0.0
    if fidelidade and combo:
        # RN-02: aplica o maior desconto (combo = 15% > fidelidade = 10%)
        percentual_desconto = DESCONTO_SERVICO_COMBO
        tipo_desconto = "Combo (maior desconto aplicado)"
    elif fidelidade:
        percentual_desconto = DESCONTO_CLIENTE_FIDELIDADE
        tipo_desconto = "Fidelidade"
    elif combo:
        percentual_desconto = DESCONTO_SERVICO_COMBO
        tipo_desconto = "Combo"
    else:
        tipo_desconto = "Sem desconto"

    # Passo 2 – Calcular o valor do desconto em reais
    valor_desconto = round(preco_base * percentual_desconto, 2)

    # Passo 3 – Aplicar o desconto ao preço base
    valor_com_desconto = round(preco_base - valor_desconto, 2)

    # Passo 4 – Calcular o ISS sobre o valor com desconto (RN-03)
    valor_iss = round(valor_com_desconto * ALIQUOTA_ISS, 2)

    # Passo 5 – Calcular o valor final (com desconto + ISS)
    valor_final = round(valor_com_desconto + valor_iss, 2)

    # Passo 6 – Retornar breakdown completo para transparência ao cliente
    return {
        "preco_base"          : preco_base,
        "tipo_desconto"       : tipo_desconto,
        "percentual_desconto" : percentual_desconto * 100,   # exibir como %
        "valor_desconto"      : valor_desconto,
        "valor_com_desconto"  : valor_com_desconto,
        "aliquota_iss"        : ALIQUOTA_ISS * 100,          # exibir como %
        "valor_iss"           : valor_iss,
        "valor_final"         : valor_final,
    }


def exibir_breakdown(breakdown: dict) -> None:
    """Exibe o detalhamento financeiro do serviço de forma formatada."""
    print("\n" + "=" * 50)
    print("        DETALHAMENTO FINANCEIRO DO SERVIÇO")
    print("=" * 50)
    print(f"  Preço base               : R$ {breakdown['preco_base']:>8.2f}")
    print(f"  Desconto ({breakdown['tipo_desconto']})")
    print(f"    Percentual             : {breakdown['percentual_desconto']:>6.1f}%")
    print(f"    Valor desconto         : R$ {breakdown['valor_desconto']:>8.2f}")
    print(f"  Subtotal c/ desconto     : R$ {breakdown['valor_com_desconto']:>8.2f}")
    print(f"  ISS ({breakdown['aliquota_iss']:.0f}%)                 : R$ {breakdown['valor_iss']:>8.2f}")
    print("-" * 50)
    print(f"  VALOR FINAL A PAGAR      : R$ {breakdown['valor_final']:>8.2f}")
    print("=" * 50 + "\n")


# ============================================================
# SEÇÃO 4: DEMONSTRAÇÃO DA FASE 1
# ============================================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("   FASE 1 – ESTRUTURA DE DADOS E CÁLCULO DO NEGÓCIO")
    print("   PetShop AmigoPet – Sistema de Gerenciamento")
    print("=" * 60)

    # Exibe dados do cliente de exemplo
    print("\n[CLIENTE DE EXEMPLO]")
    for chave, valor in cliente_exemplo.items():
        print(f"  {chave:<15}: {valor}")

    # Exibe dados do pet de exemplo
    print("\n[PET DE EXEMPLO]")
    for chave, valor in pet_exemplo.items():
        print(f"  {chave:<15}: {valor}")

    # Demonstração de cálculo para três cenários
    print("\n[CÁLCULO DE PRECIFICAÇÃO – BANHO GRANDE]")

    print("\nCenário 1: Cliente sem benefícios")
    b1 = calcular_valor_servico(PRECO_BANHO_GRANDE, fidelidade=False, combo=False)
    exibir_breakdown(b1)

    print("Cenário 2: Cliente com fidelidade")
    b2 = calcular_valor_servico(PRECO_BANHO_GRANDE, fidelidade=True, combo=False)
    exibir_breakdown(b2)

    print("Cenário 3: Cliente com fidelidade E combo")
    b3 = calcular_valor_servico(PRECO_BANHO_GRANDE, fidelidade=True, combo=True)
    exibir_breakdown(b3)