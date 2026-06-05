"""
=============================================================================
PROJETO DE EXTENSÃO – LINGUAGEM DE PROGRAMAÇÃO I
Disciplina: Linguagem de Programação I | Curso: Informática para Negócios | FATEC
Desenvolvido pelos alunos: Gabriel Champin - Luana Monteiro - Luigi Matheus - Walter Augusto 
Organização Parceira: PetShop AmigoPet Ltda.
Fase 2: Sistema CLI com CRUD completo, Relatórios e Alertas
=============================================================================
Descrição:
    Sistema de linha de comando (CLI) para gerenciamento completo do
    PetShop AmigoPet. Utiliza estruturas while, for, if/else, listas
    e dicionários para gerenciar clientes, pets e agendamentos.

Estruturas utilizadas:
    - while  : loop principal do menu e submenus
    - for    : iteração sobre listas de registros
    - if/else: tomada de decisão em todas as operações
    - listas : armazenamento de coleções de registros
    - dicts  : representação de entidades (clientes, pets, agendamentos)

Autor: Projeto Extensão 
=============================================================================
"""

# ============================================================
# IMPORTAÇÕES
# ============================================================
import os
import datetime
from fase1_estrutura import (
    calcular_valor_servico,
    PRECO_BANHO_PEQUENO, PRECO_BANHO_MEDIO, PRECO_BANHO_GRANDE,
    PRECO_TOSA_SIMPLES, PRECO_TOSA_COMPLETA,
    PRECO_CONSULTA_VETERINARIA, PRECO_VACINA, PRECO_HOSPEDAGEM_DIARIA,
    STATUS_AGENDADO, STATUS_EM_ANDAMENTO, STATUS_CONCLUIDO, STATUS_CANCELADO,
    PORTE_PEQUENO, PORTE_MEDIO, PORTE_GRANDE,
    LIMITE_AGENDA_DIARIA
)

# ============================================================
# ESTRUTURAS DE DADOS GLOBAIS (listas de dicionários)
# ============================================================
clientes      = []   # Lista de dicionários de clientes
pets          = []   # Lista de dicionários de pets
agendamentos  = []   # Lista de dicionários de agendamentos

# Contadores para geração de IDs únicos
_prox_id_cliente     = 1
_prox_id_pet         = 1
_prox_id_agendamento = 1


# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================

def limpar_tela():
    """Limpa o terminal para melhor experiência de uso."""
    os.system('cls' if os.name == 'nt' else 'clear')


def separador(titulo: str = "", char: str = "=", largura: int = 60) -> None:
    """Exibe um separador visual com título opcional."""
    if titulo:
        espacos = (largura - len(titulo) - 2) // 2
        print(char * espacos + f" {titulo} " + char * espacos)
    else:
        print(char * largura)


def pressione_enter():
    """Pausa a execução aguardando ação do usuário."""
    input("\n  [ENTER para continuar...]")


def proximo_id(lista: list) -> int:
    """Gera o próximo ID com base no maior existente na lista."""
    if not lista:          # se a lista está vazia
        return 1
    return max(item["id"] for item in lista) + 1   # for em compreensão


def buscar_por_id(lista: list, id_busca: int) -> dict | None:
    """Busca um registro pelo ID; retorna o dicionário ou None."""
    for item in lista:      # for: percorre todos os registros
        if item["id"] == id_busca:
            return item
    return None             # não encontrado


def tabela_linha(colunas: list, larguras: list) -> str:
    """Formata uma linha de tabela com colunas de largura fixa."""
    linha = ""
    for i, col in enumerate(colunas):   # for com índice
        largura = larguras[i] if i < len(larguras) else 15
        linha += str(col)[:largura].ljust(largura) + " | "
    return linha


# ============================================================
# MÓDULO: GERENCIAMENTO DE CLIENTES
# ============================================================

def cadastrar_cliente():
    """Cadastra um novo cliente no sistema."""
    separador("CADASTRAR CLIENTE")
    print()

    # Coleta e validação dos dados
    nome = input("  Nome completo      : ").strip()
    if not nome:                          # if: validação obrigatória
        print("  [ERRO] Nome não pode ser vazio.")
        return

    cpf  = input("  CPF (ex: 000.000.000-00): ").strip()
    if not cpf:
        print("  [ERRO] CPF não pode ser vazio.")
        return

    # Verifica CPF duplicado (for: percorre todos os clientes)
    for c in clientes:
        if c["cpf"] == cpf:
            print(f"  [ERRO] CPF {cpf} já cadastrado (ID {c['id']}).")
            return

    telefone = input("  Telefone           : ").strip()
    email    = input("  E-mail             : ").strip()

    # Pergunta sobre fidelidade
    fid_input = input("  Programa fidelidade? (s/n): ").strip().lower()
    fidelidade = True if fid_input == "s" else False  # if/else inline

    # Cria o dicionário do novo cliente
    novo_cliente = {
        "id"        : proximo_id(clientes),
        "nome"      : nome,
        "cpf"       : cpf,
        "telefone"  : telefone,
        "email"     : email,
        "fidelidade": fidelidade,
        "pets"      : [],
        "data_cad"  : datetime.date.today().isoformat(),
    }

    clientes.append(novo_cliente)   # adiciona à lista global
    print(f"\n  [OK] Cliente '{nome}' cadastrado com ID {novo_cliente['id']}.")


def consultar_cliente():
    """Consulta e exibe dados de um cliente pelo ID ou nome."""
    separador("CONSULTAR CLIENTE")
    print()
    termo = input("  Digite ID ou parte do nome: ").strip()

    encontrados = []   # lista local de resultados

    # Tenta busca por ID numérico
    if termo.isdigit():
        c = buscar_por_id(clientes, int(termo))
        if c:
            encontrados.append(c)
    else:
        # Busca por nome parcial (for com if)
        for c in clientes:
            if termo.lower() in c["nome"].lower():
                encontrados.append(c)

    if not encontrados:   # if: nenhum resultado
        print("  [INFO] Nenhum cliente encontrado.")
        return

    for c in encontrados:   # for: exibe cada resultado
        print()
        separador("DADOS DO CLIENTE", "-")
        print(f"  ID          : {c['id']}")
        print(f"  Nome        : {c['nome']}")
        print(f"  CPF         : {c['cpf']}")
        print(f"  Telefone    : {c['telefone']}")
        print(f"  E-mail      : {c['email']}")
        print(f"  Fidelidade  : {'SIM' if c['fidelidade'] else 'NÃO'}")
        print(f"  Pets        : {', '.join(c['pets']) if c['pets'] else 'nenhum'}")
        print(f"  Cadastro    : {c['data_cad']}")


def listar_clientes():
    """Lista todos os clientes em formato de tabela."""
    separador("LISTAGEM DE CLIENTES")
    print()

    if not clientes:   # if: lista vazia
        print("  [INFO] Nenhum cliente cadastrado.")
        return

    # Cabeçalho da tabela
    larguras = [5, 25, 16, 16, 8]
    print(tabela_linha(["ID", "Nome", "CPF", "Telefone", "Fidelid."], larguras))
    print("-" * 80)

    # Corpo da tabela (for: itera sobre todos os clientes)
    for c in clientes:
        fid = "SIM" if c["fidelidade"] else "NÃO"
        print(tabela_linha(
            [c["id"], c["nome"], c["cpf"], c["telefone"], fid],
            larguras
        ))

    print(f"\n  Total: {len(clientes)} cliente(s).")


def alterar_cliente():
    """Altera dados de um cliente existente."""
    separador("ALTERAR CLIENTE")
    print()

    id_str = input("  ID do cliente a alterar: ").strip()
    if not id_str.isdigit():
        print("  [ERRO] ID inválido.")
        return

    cliente = buscar_por_id(clientes, int(id_str))
    if not cliente:      # if: não encontrado
        print("  [ERRO] Cliente não encontrado.")
        return

    print(f"\n  Editando: {cliente['nome']} (deixe em branco para manter)")
    print()

    # Cada campo pode ser alterado individualmente (if/else por campo)
    novo_nome = input(f"  Nome [{cliente['nome']}]: ").strip()
    if novo_nome:
        cliente["nome"] = novo_nome

    novo_tel = input(f"  Telefone [{cliente['telefone']}]: ").strip()
    if novo_tel:
        cliente["telefone"] = novo_tel

    novo_email = input(f"  E-mail [{cliente['email']}]: ").strip()
    if novo_email:
        cliente["email"] = novo_email

    nova_fid = input(f"  Fidelidade [{'s' if cliente['fidelidade'] else 'n'}] (s/n): ").strip().lower()
    if nova_fid in ("s", "n"):
        cliente["fidelidade"] = nova_fid == "s"

    print(f"\n  [OK] Cliente ID {cliente['id']} atualizado com sucesso.")


def excluir_cliente():
    """Exclui um cliente após confirmação."""
    separador("EXCLUIR CLIENTE")
    print()

    id_str = input("  ID do cliente a excluir: ").strip()
    if not id_str.isdigit():
        print("  [ERRO] ID inválido.")
        return

    cliente = buscar_por_id(clientes, int(id_str))
    if not cliente:
        print("  [ERRO] Cliente não encontrado.")
        return

    # Verifica se há agendamentos ativos (for com if)
    agendamentos_ativos = []
    for ag in agendamentos:
        if ag["id_cliente"] == cliente["id"] and ag["status"] in (STATUS_AGENDADO, STATUS_EM_ANDAMENTO):
            agendamentos_ativos.append(ag)

    if agendamentos_ativos:   # if: há pendências
        print(f"  [AVISO] Cliente possui {len(agendamentos_ativos)} agendamento(s) ativo(s).")
        print("  Conclua ou cancele-os antes de excluir o cliente.")
        return

    print(f"\n  Cliente: {cliente['nome']} | CPF: {cliente['cpf']}")
    confirma = input("  Confirmar exclusão? (s/n): ").strip().lower()

    if confirma == "s":
        clientes.remove(cliente)   # remove da lista
        print("  [OK] Cliente excluído com sucesso.")
    else:
        print("  [INFO] Operação cancelada.")


# ============================================================
# MÓDULO: GERENCIAMENTO DE PETS
# ============================================================

def cadastrar_pet():
    """Cadastra um novo pet vinculado a um cliente."""
    separador("CADASTRAR PET")
    print()

    id_cli_str = input("  ID do cliente proprietário: ").strip()
    if not id_cli_str.isdigit():
        print("  [ERRO] ID inválido.")
        return

    cliente = buscar_por_id(clientes, int(id_cli_str))
    if not cliente:
        print("  [ERRO] Cliente não encontrado.")
        return

    nome_pet = input("  Nome do pet           : ").strip()
    if not nome_pet:
        print("  [ERRO] Nome obrigatório.")
        return

    especie  = input("  Espécie (Cão/Gato/Outro): ").strip().capitalize()
    raca     = input("  Raça                  : ").strip()

    # Seleção de porte com validação (while + if/else)
    print("  Porte: [1] Pequeno  [2] Médio  [3] Grande")
    porte = ""
    while not porte:   # while: repete até entrada válida
        op = input("  Opção: ").strip()
        if op == "1":
            porte = PORTE_PEQUENO
        elif op == "2":
            porte = PORTE_MEDIO
        elif op == "3":
            porte = PORTE_GRANDE
        else:
            print("  [ERRO] Opção inválida.")

    idade_str = input("  Idade (anos)          : ").strip()
    idade = int(idade_str) if idade_str.isdigit() else 0

    peso_str = input("  Peso (kg, ex: 5.2)    : ").strip()
    try:
        peso = float(peso_str)
    except ValueError:
        peso = 0.0

    novo_pet = {
        "id"        : proximo_id(pets),
        "nome"      : nome_pet,
        "especie"   : especie,
        "raca"      : raca,
        "porte"     : porte,
        "idade"     : idade,
        "peso_kg"   : peso,
        "id_cliente": cliente["id"],
    }

    pets.append(novo_pet)
    cliente["pets"].append(nome_pet)   # atualiza a lista de pets do cliente

    print(f"\n  [OK] Pet '{nome_pet}' cadastrado com ID {novo_pet['id']}.")


def listar_pets():
    """Lista todos os pets ou filtra por cliente."""
    separador("LISTAGEM DE PETS")
    print()

    filtro = input("  Filtrar por ID do cliente (ENTER para todos): ").strip()

    lista_exibir = []
    if filtro.isdigit():       # if: aplica filtro
        id_cli = int(filtro)
        for p in pets:         # for: filtra a lista
            if p["id_cliente"] == id_cli:
                lista_exibir.append(p)
    else:                      # else: sem filtro
        lista_exibir = pets

    if not lista_exibir:
        print("  [INFO] Nenhum pet encontrado.")
        return

    larguras = [5, 15, 10, 20, 10, 6, 8]
    print(tabela_linha(["ID", "Nome", "Espécie", "Raça", "Porte", "Idade", "Peso"], larguras))
    print("-" * 90)

    for p in lista_exibir:    # for: exibe cada pet
        print(tabela_linha(
            [p["id"], p["nome"], p["especie"], p["raca"],
             p["porte"], f'{p["idade"]}a', f'{p["peso_kg"]}kg'],
            larguras
        ))

    print(f"\n  Total: {len(lista_exibir)} pet(s).")


# ============================================================
# MÓDULO: GERENCIAMENTO DE AGENDAMENTOS
# ============================================================

# Tabela de serviços disponíveis (dicionário de opções)
SERVICOS_DISPONÍVEIS = {
    "1": ("Banho Pequeno",         PRECO_BANHO_PEQUENO),
    "2": ("Banho Médio",           PRECO_BANHO_MEDIO),
    "3": ("Banho Grande",          PRECO_BANHO_GRANDE),
    "4": ("Tosa Simples",          PRECO_TOSA_SIMPLES),
    "5": ("Tosa Completa",         PRECO_TOSA_COMPLETA),
    "6": ("Consulta Veterinária",  PRECO_CONSULTA_VETERINARIA),
    "7": ("Vacina",                PRECO_VACINA),
    "8": ("Hospedagem (diária)",   PRECO_HOSPEDAGEM_DIARIA),
}


def cadastrar_agendamento():
    """Cria um novo agendamento de serviço."""
    separador("NOVO AGENDAMENTO")
    print()

    # Seleciona cliente
    id_cli_str = input("  ID do cliente: ").strip()
    if not id_cli_str.isdigit():
        print("  [ERRO] ID inválido."); return
    cliente = buscar_por_id(clientes, int(id_cli_str))
    if not cliente:
        print("  [ERRO] Cliente não encontrado."); return

    # Seleciona pet do cliente
    pets_cliente = [p for p in pets if p["id_cliente"] == cliente["id"]]
    if not pets_cliente:   # if: cliente sem pets
        print("  [AVISO] Este cliente não possui pets cadastrados.")
        return

    print(f"\n  Pets de {cliente['nome']}:")
    for p in pets_cliente:   # for: exibe pets disponíveis
        print(f"    [{p['id']}] {p['nome']} ({p['especie']} – {p['porte']})")

    id_pet_str = input("  ID do pet: ").strip()
    if not id_pet_str.isdigit():
        print("  [ERRO] ID inválido."); return
    pet = buscar_por_id(pets, int(id_pet_str))
    if not pet or pet["id_cliente"] != cliente["id"]:
        print("  [ERRO] Pet não encontrado ou não pertence a este cliente."); return

    # Seleciona serviço
    print("\n  Serviços disponíveis:")
    for cod, (nome_srv, preco) in SERVICOS_DISPONÍVEIS.items():
        print(f"    [{cod}] {nome_srv:<30} R$ {preco:.2f}")
    cod_srv = input("  Código do serviço: ").strip()

    if cod_srv not in SERVICOS_DISPONÍVEIS:
        print("  [ERRO] Serviço inválido."); return

    nome_servico, preco_base = SERVICOS_DISPONÍVEIS[cod_srv]

    # Combo?
    combo_input = input("  É um combo? (s/n): ").strip().lower()
    combo = combo_input == "s"

    # Calcula valor final
    breakdown = calcular_valor_servico(preco_base, cliente["fidelidade"], combo)

    # Data e hora
    data = input("  Data (AAAA-MM-DD): ").strip()
    hora = input("  Hora (HH:MM)     : ").strip()

    # Verifica lotação da agenda naquele dia (for com contador)
    count_dia = 0
    for ag in agendamentos:
        if ag["data"] == data and ag["status"] != STATUS_CANCELADO:
            count_dia += 1

    if count_dia >= LIMITE_AGENDA_DIARIA:   # if: agenda cheia
        print(f"  [ALERTA] Agenda do dia {data} está lotada ({LIMITE_AGENDA_DIARIA} atendimentos).")
        continuar = input("  Deseja forçar o agendamento mesmo assim? (s/n): ").strip().lower()
        if continuar != "s":
            return

    obs = input("  Observações (opcional): ").strip()

    novo_ag = {
        "id"         : proximo_id(agendamentos),
        "id_cliente" : cliente["id"],
        "nome_cliente": cliente["nome"],
        "id_pet"     : pet["id"],
        "nome_pet"   : pet["nome"],
        "servico"    : nome_servico,
        "data"        : data,
        "hora"        : hora,
        "status"     : STATUS_AGENDADO,
        "valor_bruto" : preco_base,
        "valor_final" : breakdown["valor_final"],
        "desconto"   : breakdown["valor_desconto"],
        "observacoes": obs,
    }

    agendamentos.append(novo_ag)
    print(f"\n  [OK] Agendamento #{novo_ag['id']} criado.")
    print(f"       Serviço : {nome_servico}")
    print(f"       Data/Hora: {data} às {hora}")
    print(f"       Valor final: R$ {breakdown['valor_final']:.2f}")


def listar_agendamentos():
    """Lista todos os agendamentos com filtro por status."""
    separador("LISTAGEM DE AGENDAMENTOS")
    print()
    print("  Filtrar: [1] Todos  [2] Agendados  [3] Em Andamento  [4] Concluídos  [5] Cancelados")
    op = input("  Opção: ").strip()

    # Dicionário de filtros (mapeamento opção → status)
    filtros = {
        "1": None,
        "2": STATUS_AGENDADO,
        "3": STATUS_EM_ANDAMENTO,
        "4": STATUS_CONCLUIDO,
        "5": STATUS_CANCELADO,
    }

    status_filtro = filtros.get(op)   # None = sem filtro

    lista_exibir = []
    for ag in agendamentos:   # for: aplica filtro
        if status_filtro is None or ag["status"] == status_filtro:
            lista_exibir.append(ag)

    if not lista_exibir:
        print("  [INFO] Nenhum agendamento encontrado.")
        return

    larguras = [5, 20, 12, 10, 10, 22, 12]
    print(tabela_linha(["ID", "Cliente", "Pet", "Data", "Hora", "Serviço", "Status"], larguras))
    print("-" * 100)

    for ag in lista_exibir:   # for: exibe cada linha
        print(tabela_linha(
            [ag["id"], ag["nome_cliente"], ag["nome_pet"],
             ag["data"], ag["hora"], ag["servico"], ag["status"]],
            larguras
        ))

    print(f"\n  Total: {len(lista_exibir)} agendamento(s).")


def alterar_status_agendamento():
    """Altera o status de um agendamento existente."""
    separador("ALTERAR STATUS DE AGENDAMENTO")
    print()

    id_str = input("  ID do agendamento: ").strip()
    if not id_str.isdigit():
        print("  [ERRO] ID inválido."); return

    ag = buscar_por_id(agendamentos, int(id_str))
    if not ag:
        print("  [ERRO] Agendamento não encontrado."); return

    print(f"\n  Agendamento #{ag['id']}: {ag['servico']} – {ag['data']}")
    print(f"  Status atual: {ag['status']}")
    print(f"\n  Novo status: [1] Agendado  [2] Em Andamento  [3] Concluído  [4] Cancelado")

    opcoes_status = {
        "1": STATUS_AGENDADO,
        "2": STATUS_EM_ANDAMENTO,
        "3": STATUS_CONCLUIDO,
        "4": STATUS_CANCELADO,
    }

    op = input("  Opção: ").strip()
    if op not in opcoes_status:   # if: opção inválida
        print("  [ERRO] Opção inválida."); return

    ag["status"] = opcoes_status[op]
    print(f"  [OK] Status atualizado para '{ag['status']}'.")


def excluir_agendamento():
    """Exclui (cancela) um agendamento."""
    separador("EXCLUIR AGENDAMENTO")
    print()

    id_str = input("  ID do agendamento a excluir: ").strip()
    if not id_str.isdigit():
        print("  [ERRO] ID inválido."); return

    ag = buscar_por_id(agendamentos, int(id_str))
    if not ag:
        print("  [ERRO] Agendamento não encontrado."); return

    if ag["status"] == STATUS_CONCLUIDO:   # if: não pode excluir concluído
        print("  [ERRO] Agendamentos concluídos não podem ser excluídos, apenas visualizados.")
        return

    print(f"\n  Agendamento #{ag['id']}: {ag['servico']} de {ag['nome_pet']}")
    confirma = input("  Confirmar exclusão? (s/n): ").strip().lower()

    if confirma == "s":
        agendamentos.remove(ag)
        print("  [OK] Agendamento excluído.")
    else:
        print("  [INFO] Operação cancelada.")


# ============================================================
# MÓDULO: RELATÓRIOS
# ============================================================

def relatorio_faturamento():
    """Gera relatório de faturamento por período."""
    separador("RELATÓRIO DE FATURAMENTO")
    print()

    data_ini = input("  Data inicial (AAAA-MM-DD, ENTER=todos): ").strip()
    data_fim = input("  Data final   (AAAA-MM-DD, ENTER=todos): ").strip()

    total_bruto  = 0.0
    total_descon = 0.0
    total_final  = 0.0
    count        = 0

    print()
    larguras = [5, 12, 15, 25, 10, 10]
    print(tabela_linha(["ID", "Data", "Pet", "Serviço", "Bruto", "Final"], larguras))
    print("-" * 85)

    for ag in agendamentos:   # for: percorre todos os agendamentos
        # Filtro de data (if com condições compostas)
        if data_ini and ag["data"] < data_ini:
            continue
        if data_fim and ag["data"] > data_fim:
            continue
        if ag["status"] != STATUS_CONCLUIDO:   # só conta serviços concluídos
            continue

        print(tabela_linha(
            [ag["id"], ag["data"], ag["nome_pet"], ag["servico"],
             f'R${ag["valor_bruto"]:.2f}', f'R${ag["valor_final"]:.2f}'],
            larguras
        ))

        total_bruto  += ag["valor_bruto"]
        total_descon += ag["desconto"]
        total_final  += ag["valor_final"]
        count        += 1

    # Totalizador
    print("=" * 85)
    print(f"  Serviços concluídos : {count}")
    print(f"  Faturamento bruto   : R$ {total_bruto:.2f}")
    print(f"  Descontos concedidos: R$ {total_descon:.2f}")
    print(f"  FATURAMENTO LÍQUIDO : R$ {total_final:.2f}")


def relatorio_servicos_populares():
    """Exibe ranking dos serviços mais solicitados."""
    separador("SERVIÇOS MAIS POPULARES")
    print()

    contagem = {}   # dicionário de contagem

    for ag in agendamentos:   # for: conta cada serviço
        srv = ag["servico"]
        if srv in contagem:   # if: já existe no dict
            contagem[srv] += 1
        else:                 # else: primeira ocorrência
            contagem[srv] = 1

    if not contagem:
        print("  [INFO] Nenhum agendamento registrado.")
        return

    # Ordena por quantidade decrescente
    ranking = sorted(contagem.items(), key=lambda x: x[1], reverse=True)

    print(f"  {'Serviço':<35} {'Qtd':>5}")
    print("-" * 45)
    for srv, qtd in ranking:   # for: exibe ranking
        barra = "█" * qtd
        print(f"  {srv:<35} {qtd:>5}  {barra}")


# ============================================================
# MÓDULO: ALERTAS AUTOMÁTICOS
# ============================================================

def verificar_alertas():
    """Verifica e exibe alertas automáticos do sistema."""
    separador("ALERTAS DO SISTEMA", "!")
    alertas_gerados = 0

    hoje = datetime.date.today().isoformat()

    # ALERTA 1: Agendamentos do dia
    ag_hoje = []
    for ag in agendamentos:   # for: filtra agendamentos de hoje
        if ag["data"] == hoje and ag["status"] == STATUS_AGENDADO:
            ag_hoje.append(ag)

    if ag_hoje:   # if: há agendamentos hoje
        print(f"\n  [!] {len(ag_hoje)} agendamento(s) para HOJE ({hoje}):")
        for ag in ag_hoje:   # for: lista cada um
            print(f"      → {ag['hora']} | {ag['nome_pet']} | {ag['servico']}")
        alertas_gerados += 1

    # ALERTA 2: Verificar lotação do dia
    count_hoje = 0
    for ag in agendamentos:
        if ag["data"] == hoje and ag["status"] != STATUS_CANCELADO:
            count_hoje += 1

    if count_hoje >= LIMITE_AGENDA_DIARIA * 0.8:   # 80% da capacidade
        print(f"\n  [!] ALERTA DE LOTAÇÃO: Agenda de hoje com {count_hoje}/{LIMITE_AGENDA_DIARIA} atendimentos.")
        alertas_gerados += 1

    # ALERTA 3: Agendamentos sem status atualizado há mais de 1 dia
    for ag in agendamentos:   # for: verifica status desatualizados
        if ag["status"] == STATUS_EM_ANDAMENTO and ag["data"] < hoje:
            print(f"\n  [!] Agendamento #{ag['id']} ainda 'Em Andamento' (data: {ag['data']}).")
            alertas_gerados += 1

    if alertas_gerados == 0:   # if: sem alertas
        print("\n  [✓] Nenhum alerta no momento. Sistema operando normalmente.")


# ============================================================
# MENUS
# ============================================================

def menu_clientes():
    """Submenu de gerenciamento de clientes."""
    while True:   # while: loop do submenu
        limpar_tela()
        separador("MENU – CLIENTES")
        print("  [1] Cadastrar cliente")
        print("  [2] Consultar cliente")
        print("  [3] Listar clientes")
        print("  [4] Alterar cliente")
        print("  [5] Excluir cliente")
        print("  [0] Voltar")
        separador()

        op = input("  Opção: ").strip()

        if op == "1":
            cadastrar_cliente()
        elif op == "2":
            consultar_cliente()
        elif op == "3":
            listar_clientes()
        elif op == "4":
            alterar_cliente()
        elif op == "5":
            excluir_cliente()
        elif op == "0":
            break   # sai do while do submenu
        else:
            print("  [ERRO] Opção inválida.")

        pressione_enter()


def menu_pets():
    """Submenu de gerenciamento de pets."""
    while True:
        limpar_tela()
        separador("MENU – PETS")
        print("  [1] Cadastrar pet")
        print("  [2] Listar pets")
        print("  [0] Voltar")
        separador()

        op = input("  Opção: ").strip()

        if op == "1":
            cadastrar_pet()
        elif op == "2":
            listar_pets()
        elif op == "0":
            break
        else:
            print("  [ERRO] Opção inválida.")

        pressione_enter()


def menu_agendamentos():
    """Submenu de gerenciamento de agendamentos."""
    while True:
        limpar_tela()
        separador("MENU – AGENDAMENTOS")
        print("  [1] Novo agendamento")
        print("  [2] Listar agendamentos")
        print("  [3] Alterar status")
        print("  [4] Excluir agendamento")
        print("  [0] Voltar")
        separador()

        op = input("  Opção: ").strip()

        if op == "1":
            cadastrar_agendamento()
        elif op == "2":
            listar_agendamentos()
        elif op == "3":
            alterar_status_agendamento()
        elif op == "4":
            excluir_agendamento()
        elif op == "0":
            break
        else:
            print("  [ERRO] Opção inválida.")

        pressione_enter()


def menu_relatorios():
    """Submenu de relatórios."""
    while True:
        limpar_tela()
        separador("MENU – RELATÓRIOS")
        print("  [1] Faturamento por período")
        print("  [2] Serviços mais populares")
        print("  [0] Voltar")
        separador()

        op = input("  Opção: ").strip()

        if op == "1":
            relatorio_faturamento()
        elif op == "2":
            relatorio_servicos_populares()
        elif op == "0":
            break
        else:
            print("  [ERRO] Opção inválida.")

        pressione_enter()


def carregar_dados_exemplo():
    """Popula o sistema com dados de exemplo para demonstração."""
    global clientes, pets, agendamentos

    clientes = [
        {"id": 1, "nome": "Maria Oliveira",  "cpf": "111.222.333-44",
         "telefone": "(11) 98765-4321", "email": "maria@email.com",
         "fidelidade": True,  "pets": ["Thor"], "data_cad": "2024-01-10"},
        {"id": 2, "nome": "João Santos",     "cpf": "555.666.777-88",
         "telefone": "(11) 91234-5678", "email": "joao@email.com",
         "fidelidade": False, "pets": ["Mel"],  "data_cad": "2024-03-22"},
        {"id": 3, "nome": "Ana Costa",       "cpf": "999.000.111-22",
         "telefone": "(11) 97777-1234", "email": "ana@email.com",
         "fidelidade": True,  "pets": ["Bolinha", "Neve"], "data_cad": "2023-11-05"},
    ]

    pets = [
        {"id": 1, "nome": "Thor",    "especie": "Cão",  "raca": "Golden Retriever",
         "porte": PORTE_GRANDE,   "idade": 3, "peso_kg": 28.5, "id_cliente": 1},
        {"id": 2, "nome": "Mel",     "especie": "Cão",  "raca": "Poodle",
         "porte": PORTE_PEQUENO,  "idade": 5, "peso_kg": 4.2,  "id_cliente": 2},
        {"id": 3, "nome": "Bolinha", "especie": "Gato", "raca": "SRD",
         "porte": PORTE_PEQUENO,  "idade": 2, "peso_kg": 3.8,  "id_cliente": 3},
        {"id": 4, "nome": "Neve",    "especie": "Gato", "raca": "Persa",
         "porte": PORTE_MEDIO,    "idade": 4, "peso_kg": 5.0,  "id_cliente": 3},
    ]

    hoje = datetime.date.today().isoformat()
    agendamentos = [
        {"id": 1, "id_cliente": 1, "nome_cliente": "Maria Oliveira",
         "id_pet": 1, "nome_pet": "Thor", "servico": "Banho Grande",
         "data": hoje, "hora": "09:00", "status": STATUS_AGENDADO,
         "valor_bruto": 90.0, "valor_final": 85.05, "desconto": 9.0,
         "observacoes": "Alérgico a determinados shampoos"},
        {"id": 2, "id_cliente": 2, "nome_cliente": "João Santos",
         "id_pet": 2, "nome_pet": "Mel", "servico": "Tosa Completa",
         "data": "2025-08-10", "hora": "14:00", "status": STATUS_CONCLUIDO,
         "valor_bruto": 85.0, "valor_final": 89.25, "desconto": 0.0,
         "observacoes": ""},
        {"id": 3, "id_cliente": 3, "nome_cliente": "Ana Costa",
         "id_pet": 3, "nome_pet": "Bolinha", "servico": "Consulta Veterinária",
         "data": "2025-08-12", "hora": "11:30", "status": STATUS_AGENDADO,
         "valor_bruto": 150.0, "valor_final": 141.75, "desconto": 15.0,
         "observacoes": "Check-up anual"},
    ]


# ============================================================
# MENU PRINCIPAL / PONTO DE ENTRADA
# ============================================================

def main():
    """Função principal – ponto de entrada do sistema CLI."""
    carregar_dados_exemplo()   # carrega dados para demonstração

    while True:   # while principal: mantém o sistema rodando
        limpar_tela()
        separador("SISTEMA AMIGOPET – v1.0")
        print("  [1] Gerenciar Clientes")
        print("  [2] Gerenciar Pets")
        print("  [3] Gerenciar Agendamentos")
        print("  [4] Relatórios")
        print("  [5] Verificar Alertas")
        print("  [0] Encerrar Sistema")
        separador()

        op = input("  Opção: ").strip()

        if op == "1":
            menu_clientes()
        elif op == "2":
            menu_pets()
        elif op == "3":
            menu_agendamentos()
        elif op == "4":
            menu_relatorios()
        elif op == "5":
            verificar_alertas()
            pressione_enter()
        elif op == "0":
            # Encerramento do sistema
            print("\n  Encerrando sistema AmigoPet...")
            print("  Obrigado por utilizar nosso sistema!")
            print("  Até logo!\n")
            break    # encerra o while principal
        else:
            print("  [ERRO] Opção inválida.")
            pressione_enter()


if __name__ == "__main__":
    main()