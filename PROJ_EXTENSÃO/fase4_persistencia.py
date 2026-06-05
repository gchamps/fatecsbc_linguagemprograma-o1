"""
=============================================================================
PROJETO DE EXTENSÃO – LINGUAGEM DE PROGRAMAÇÃO I
Disciplina: Linguagem de Programação I | Curso: Informática para Negócios | FATEC
Desenvolvido pelos alunos: Gabriel Champin - Luana Monteiro - Luigi Matheus - Walter Augusto 
Organização Parceira: PetShop AmigoPet Ltda.
Fase 4: Persistência de Dados (CSV e TXT) + Tratamento de Exceções
=============================================================================
Descrição:
    Implementação completa de persistência com:
      • Leitura automática ao iniciar o sistema
      • Salvamento automático ao encerrar
      • Persistência em formato CSV (tabular)
      • Persistência em formato TXT (log/relatório)
      • Tratamento completo de exceções:
          - ValueError  : dados inválidos na leitura/conversão
          - TypeError   : tipo de dado inesperado
          - FileNotFoundError : arquivo não existe (primeira execução)
          - Exception   : erros genéricos inesperados

Autor: Projeto Extensão
=============================================================================
"""

import csv
import os
import datetime
from fase3_poo import (
    Cliente, Pet, Cao, Gato, Agendamento,
    RepositorioClientes, RepositorioPets, RepositorioAgendamentos,
    ServicoCalculadora, CPFInvalidoError, AgendamentoInvalidoError
)
from fase1_estrutura import (
    STATUS_AGENDADO, STATUS_EM_ANDAMENTO, STATUS_CONCLUIDO, STATUS_CANCELADO,
    PORTE_PEQUENO, PORTE_MEDIO, PORTE_GRANDE, LIMITE_AGENDA_DIARIA
)

# ============================================================
# CONFIGURAÇÃO DE CAMINHOS
# ============================================================

PASTA_DADOS    = "dados"
ARQ_CLIENTES   = os.path.join(PASTA_DADOS, "clientes.csv")
ARQ_PETS       = os.path.join(PASTA_DADOS, "pets.csv")
ARQ_AGEND      = os.path.join(PASTA_DADOS, "agendamentos.csv")
ARQ_LOG        = os.path.join(PASTA_DADOS, "log_operacoes.txt")
ARQ_RELATORIO  = os.path.join(PASTA_DADOS, "relatorio_diario.txt")


def garantir_pasta_dados() -> None:
    """Cria a pasta 'dados' se não existir."""
    if not os.path.exists(PASTA_DADOS):
        os.makedirs(PASTA_DADOS)
        registrar_log("SISTEMA", "Pasta 'dados' criada automaticamente.")


# ============================================================
# MÓDULO DE LOG (TXT)
# ============================================================

def registrar_log(operacao: str, detalhe: str) -> None:
    """
    Registra uma operação no arquivo de log TXT.

    Trata FileNotFoundError (pasta não existe) e Exception genérica.
    """
    try:
        garantir_pasta_dados()
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        linha = f"[{timestamp}] [{operacao:^20}] {detalhe}\n"
        with open(ARQ_LOG, "a", encoding="utf-8") as f:
            f.write(linha)
    except FileNotFoundError as e:
        # Incomum após garantir_pasta_dados(), mas tratado defensivamente
        print(f"  [AVISO] Log: pasta não encontrada – {e}")
    except Exception as e:
        # Falha de log não deve interromper o fluxo principal
        print(f"  [AVISO] Falha ao registrar log: {e}")


# ============================================================
# PERSISTÊNCIA EM CSV – CLIENTES
# ============================================================

CABECALHO_CLIENTES = [
    "id", "nome", "cpf", "telefone", "email",
    "fidelidade", "pets", "data_cad"
]


def salvar_clientes(repo: RepositorioClientes) -> bool:
    """
    Salva todos os clientes em CSV.

    Exceções tratadas:
        TypeError       : objeto inválido na lista
        Exception       : erro genérico de I/O
    """
    try:
        garantir_pasta_dados()
        with open(ARQ_CLIENTES, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=CABECALHO_CLIENTES)
            writer.writeheader()
            for c in repo.listar_todos():
                try:
                    d = c.to_dict()
                    # Converte lista de pets para string separada por |
                    d["pets"] = "|".join(d["pets"])
                    writer.writerow(d)
                except TypeError as e:
                    # Pula registro inválido sem interromper os demais
                    print(f"  [AVISO] Tipo inválido no cliente ID {getattr(c, 'id', '?')}: {e}")
                    registrar_log("ERRO_TIPO", f"Cliente inválido: {e}")
        registrar_log("SALVAR", f"Clientes: {len(repo)} registro(s) salvos em {ARQ_CLIENTES}")
        return True
    except Exception as e:
        print(f"  [ERRO] Falha ao salvar clientes: {e}")
        registrar_log("ERRO", f"salvar_clientes: {e}")
        return False


def carregar_clientes(repo: RepositorioClientes) -> int:
    """
    Carrega clientes do arquivo CSV para o repositório.

    Exceções tratadas:
        FileNotFoundError : arquivo não existe (primeira execução)
        ValueError        : dado inválido (ex: ID não numérico, CPF mal formado)
        TypeError         : campo com tipo inesperado
        Exception         : erro genérico
    """
    count_ok  = 0
    count_err = 0

    try:
        with open(ARQ_CLIENTES, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for numero_linha, row in enumerate(reader, start=2):
                try:
                    # ValueError se id não for inteiro
                    id_ = int(row["id"])
                    # Reconstrói lista de pets
                    pets_lista = row["pets"].split("|") if row.get("pets") else []
                    # ValueError / CPFInvalidoError se CPF mal formado
                    cliente = Cliente(
                        id_           = id_,
                        nome          = row["nome"],
                        cpf           = row["cpf"],
                        telefone      = row["telefone"],
                        email         = row.get("email", ""),
                        fidelidade    = row.get("fidelidade", "False") == "True",
                    )
                    # Restaura lista de pets diretamente (bypass do setter)
                    cliente.__dict__["_Cliente__pets"]    = pets_lista
                    cliente.__dict__["_Cliente__data_cad"] = row.get("data_cad", "")
                    repo.adicionar(cliente)
                    count_ok += 1

                except (ValueError, CPFInvalidoError) as e:
                    count_err += 1
                    print(f"  [AVISO] Linha {numero_linha} ignorada (dado inválido): {e}")
                    registrar_log("ERRO_LEITURA", f"clientes.csv L{numero_linha}: {e}")

                except (TypeError, KeyError) as e:
                    count_err += 1
                    print(f"  [AVISO] Linha {numero_linha} ignorada (campo ausente): {e}")
                    registrar_log("ERRO_LEITURA", f"clientes.csv L{numero_linha}: {e}")

    except FileNotFoundError:
        # Primeira execução: arquivo ainda não existe
        registrar_log("INFO", "clientes.csv não encontrado – iniciando banco vazio.")

    except Exception as e:
        print(f"  [ERRO] Falha ao carregar clientes: {e}")
        registrar_log("ERRO", f"carregar_clientes: {e}")

    if count_ok:
        registrar_log("CARREGAR", f"Clientes: {count_ok} carregado(s), {count_err} erro(s).")
    return count_ok


# ============================================================
# PERSISTÊNCIA EM CSV – PETS
# ============================================================

CABECALHO_PETS = [
    "id", "nome", "especie", "raca", "porte",
    "idade", "peso_kg", "id_cliente"
]


def salvar_pets(repo: RepositorioPets) -> bool:
    """Salva todos os pets em CSV com tratamento de exceções."""
    try:
        garantir_pasta_dados()
        with open(ARQ_PETS, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=CABECALHO_PETS)
            writer.writeheader()
            for p in repo.listar_todos():
                try:
                    d = p.to_dict()
                    # Mantém apenas os campos do cabeçalho
                    row = {k: d[k] for k in CABECALHO_PETS}
                    writer.writerow(row)
                except (TypeError, KeyError) as e:
                    print(f"  [AVISO] Pet ID {getattr(p, 'id', '?')} com problema: {e}")
        registrar_log("SALVAR", f"Pets: {len(repo)} registro(s) salvos.")
        return True
    except Exception as e:
        print(f"  [ERRO] Falha ao salvar pets: {e}")
        registrar_log("ERRO", f"salvar_pets: {e}")
        return False


def carregar_pets(repo: RepositorioPets) -> int:
    """Carrega pets do CSV com tratamento completo de exceções."""
    count_ok  = 0
    count_err = 0

    try:
        with open(ARQ_PETS, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for num_linha, row in enumerate(reader, start=2):
                try:
                    id_       = int(row["id"])          # ValueError se não inteiro
                    id_cli    = int(row["id_cliente"])
                    idade     = int(row["idade"])
                    peso      = float(row["peso_kg"])   # ValueError se não float
                    especie   = row["especie"]

                    # Instancia a subclasse correta com base na espécie
                    if especie.lower() == "cão":
                        pet = Cao(id_, row["nome"], row["raca"],
                                   row["porte"], idade, peso, id_cli)
                    elif especie.lower() == "gato":
                        pet = Gato(id_, row["nome"], row["raca"],
                                    row["porte"], idade, peso, id_cli)
                    else:
                        pet = Pet(id_, row["nome"], especie, row["raca"],
                                   row["porte"], idade, peso, id_cli)

                    repo.adicionar(pet)
                    count_ok += 1

                except ValueError as e:
                    count_err += 1
                    print(f"  [AVISO] Linha {num_linha} (pets) ignorada: {e}")
                    registrar_log("ERRO_LEITURA", f"pets.csv L{num_linha}: {e}")
                except (TypeError, KeyError) as e:
                    count_err += 1
                    print(f"  [AVISO] Linha {num_linha} (pets) campo ausente: {e}")

    except FileNotFoundError:
        registrar_log("INFO", "pets.csv não encontrado – iniciando banco vazio.")
    except Exception as e:
        print(f"  [ERRO] Falha ao carregar pets: {e}")
        registrar_log("ERRO", f"carregar_pets: {e}")

    return count_ok


# ============================================================
# PERSISTÊNCIA EM CSV – AGENDAMENTOS
# ============================================================

CABECALHO_AGEND = [
    "id", "id_cliente", "nome_cliente", "id_pet", "nome_pet",
    "servico", "data", "hora", "status",
    "valor_bruto", "valor_final", "desconto", "observacoes"
]


def salvar_agendamentos(repo: RepositorioAgendamentos) -> bool:
    """Salva todos os agendamentos em CSV."""
    try:
        garantir_pasta_dados()
        with open(ARQ_AGEND, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=CABECALHO_AGEND)
            writer.writeheader()
            for ag in repo.listar_todos():
                try:
                    writer.writerow(ag.to_dict())
                except (TypeError, KeyError) as e:
                    print(f"  [AVISO] Agendamento ID {ag.id} com problema: {e}")
        registrar_log("SALVAR", f"Agendamentos: {len(repo)} registro(s) salvos.")
        return True
    except Exception as e:
        print(f"  [ERRO] Falha ao salvar agendamentos: {e}")
        registrar_log("ERRO", f"salvar_agendamentos: {e}")
        return False


def carregar_agendamentos(repo: RepositorioAgendamentos) -> int:
    """Carrega agendamentos do CSV com tratamento de exceções."""
    count_ok  = 0
    count_err = 0

    try:
        with open(ARQ_AGEND, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for num_linha, row in enumerate(reader, start=2):
                try:
                    id_     = int(row["id"])
                    id_cli  = int(row["id_cliente"])
                    id_pet  = int(row["id_pet"])
                    v_bruto = float(row["valor_bruto"])
                    desc    = float(row.get("desconto", "0") or "0")

                    ag = Agendamento(
                        id_, id_cli, row["nome_cliente"],
                        id_pet, row["nome_pet"], row["servico"],
                        row["data"], row["hora"], v_bruto, desc
                    )
                    # Restaura status e outros campos via acesso direto ao __dict__
                    status_salvo = row.get("status", STATUS_AGENDADO)
                    ag.__dict__["_Agendamento__status"]      = status_salvo
                    ag.__dict__["_Agendamento__valor_final"] = float(row.get("valor_final", v_bruto - desc))
                    ag.__dict__["_Agendamento__observacoes"] = row.get("observacoes", "")

                    repo.adicionar(ag)
                    count_ok += 1

                except ValueError as e:
                    count_err += 1
                    print(f"  [AVISO] Linha {num_linha} (agend.) dado inválido: {e}")
                    registrar_log("ERRO_LEITURA", f"agendamentos.csv L{num_linha}: {e}")
                except (TypeError, KeyError) as e:
                    count_err += 1
                    print(f"  [AVISO] Linha {num_linha} (agend.) campo ausente: {e}")

    except FileNotFoundError:
        registrar_log("INFO", "agendamentos.csv não encontrado – iniciando banco vazio.")
    except Exception as e:
        print(f"  [ERRO] Falha ao carregar agendamentos: {e}")
        registrar_log("ERRO", f"carregar_agendamentos: {e}")

    return count_ok


# ============================================================
# RELATÓRIO DIÁRIO EM TXT
# ============================================================

def gerar_relatorio_txt(repo_cli: RepositorioClientes,
                         repo_pts: RepositorioPets,
                         repo_ag : RepositorioAgendamentos) -> bool:
    """
    Gera relatório diário completo em arquivo TXT.

    Exceções tratadas:
        FileNotFoundError : pasta de dados não existe
        Exception         : erro genérico de escrita
    """
    try:
        garantir_pasta_dados()
        hoje      = datetime.date.today()
        agora     = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        # Coleta dados para o relatório
        ag_hoje   = repo_ag.listar_por_data(hoje.isoformat())
        ativos    = repo_ag.listar_ativos()
        fat_total = repo_ag.faturamento_total()

        with open(ARQ_RELATORIO, "w", encoding="utf-8") as f:
            # Cabeçalho
            f.write("=" * 60 + "\n")
            f.write(f"   RELATÓRIO DIÁRIO – PETSHOP AMIGOPET\n")
            f.write(f"   Gerado em: {agora}\n")
            f.write("=" * 60 + "\n\n")

            # Sumário geral
            f.write("[SUMÁRIO GERAL]\n")
            f.write(f"  Total de clientes    : {len(repo_cli)}\n")
            f.write(f"  Total de pets        : {len(repo_pts)}\n")
            f.write(f"  Total de agendamentos: {len(repo_ag)}\n")
            f.write(f"  Agendamentos ativos  : {len(ativos)}\n")
            f.write(f"  Faturamento total    : R$ {fat_total:.2f}\n\n")

            # Agenda do dia
            f.write(f"[AGENDA DO DIA – {hoje.strftime('%d/%m/%Y')}]\n")
            if ag_hoje:
                for ag in sorted(ag_hoje, key=lambda x: x.hora):
                    f.write(f"  {ag.hora} | {ag.nome_pet:15} | {ag.servico:25} | "
                             f"{ag.status:15} | R$ {ag.valor_final:.2f}\n")
            else:
                f.write("  Nenhum agendamento para hoje.\n")
            f.write("\n")

            # Alertas
            f.write("[ALERTAS]\n")
            if len(ag_hoje) >= LIMITE_AGENDA_DIARIA * 0.8:
                f.write(f"  ⚠ Agenda com {len(ag_hoje)}/{LIMITE_AGENDA_DIARIA} atendimentos hoje.\n")
            ag_pendentes = [ag for ag in ativos if ag.data < hoje.isoformat()]
            if ag_pendentes:
                f.write(f"  ⚠ {len(ag_pendentes)} agendamento(s) de datas anteriores ainda ativo(s).\n")
            if not ag_hoje and not ag_pendentes:
                f.write("  Nenhum alerta no momento.\n")
            f.write("\n")

            # Rodapé
            f.write("=" * 60 + "\n")
            f.write("   Fim do relatório\n")
            f.write("=" * 60 + "\n")

        registrar_log("RELATORIO", f"Relatório diário gerado em {ARQ_RELATORIO}")
        return True

    except FileNotFoundError as e:
        print(f"  [ERRO] Pasta de dados não encontrada ao gerar relatório: {e}")
        return False
    except Exception as e:
        print(f"  [ERRO] Falha ao gerar relatório TXT: {e}")
        registrar_log("ERRO", f"gerar_relatorio_txt: {e}")
        return False


# ============================================================
# FUNÇÕES DE INICIALIZAÇÃO E ENCERRAMENTO
# ============================================================

def inicializar_sistema(repo_cli: RepositorioClientes,
                         repo_pts: RepositorioPets,
                         repo_ag : RepositorioAgendamentos) -> None:
    """
    Carrega todos os dados ao iniciar o sistema.
    Chamada automaticamente no startup da aplicação.
    """
    print("  Carregando dados do disco...")
    n_cli  = carregar_clientes(repo_cli)
    n_pts  = carregar_pets(repo_pts)
    n_ag   = carregar_agendamentos(repo_ag)
    print(f"  → {n_cli} cliente(s), {n_pts} pet(s), {n_ag} agendamento(s) carregados.")
    registrar_log("STARTUP", f"Sistema iniciado: {n_cli} clientes, {n_pts} pets, {n_ag} agendamentos.")


def encerrar_sistema(repo_cli: RepositorioClientes,
                      repo_pts: RepositorioPets,
                      repo_ag : RepositorioAgendamentos) -> None:
    """
    Salva todos os dados ao encerrar o sistema.
    Chamada automaticamente no shutdown da aplicação.
    Gera também o relatório diário TXT.
    """
    print("\n  Salvando dados no disco...")
    ok_cli = salvar_clientes(repo_cli)
    ok_pts = salvar_pets(repo_pts)
    ok_ag  = salvar_agendamentos(repo_ag)

    status_cli = "OK" if ok_cli else "FALHA"
    status_pts = "OK" if ok_pts else "FALHA"
    status_ag  = "OK" if ok_ag  else "FALHA"

    print(f"  → Clientes [{status_cli}] | Pets [{status_pts}] | Agendamentos [{status_ag}]")

    print("  Gerando relatório diário...")
    ok_rel = gerar_relatorio_txt(repo_cli, repo_pts, repo_ag)
    print(f"  → Relatório [{'OK' if ok_rel else 'FALHA'}]")

    registrar_log("SHUTDOWN", "Sistema encerrado normalmente.")
    print("\n  Dados salvos com sucesso. Até logo!\n")


# ============================================================
# SISTEMA COMPLETO COM PERSISTÊNCIA (INTEGRAÇÃO)
# ============================================================

def main():
    """
    Ponto de entrada do sistema completo com persistência.
    Integra Fase 3 (POO) + Fase 4 (persistência + exceções).
    """
    import os

    # Instancia repositórios
    repo_clientes    = RepositorioClientes()
    repo_pets        = RepositorioPets()
    repo_agendamentos = RepositorioAgendamentos()

    print("\n" + "=" * 60)
    print("   SISTEMA AMIGOPET – v2.0 (com Persistência)")
    print("=" * 60)

    # ── INICIALIZAÇÃO AUTOMÁTICA ──────────────────────────────
    inicializar_sistema(repo_clientes, repo_pets, repo_agendamentos)

    # ── MENU PRINCIPAL ────────────────────────────────────────
    while True:
        print("\n" + "=" * 60)
        print("  MENU PRINCIPAL")
        print("  [1] Cadastrar cliente")
        print("  [2] Listar clientes")
        print("  [3] Cadastrar pet")
        print("  [4] Listar pets")
        print("  [5] Novo agendamento")
        print("  [6] Listar agendamentos")
        print("  [7] Alterar status do agendamento")
        print("  [8] Gerar relatório TXT")
        print("  [0] Encerrar sistema")
        print("=" * 60)

        opcao = input("  Opção: ").strip()

        # ── CADASTRAR CLIENTE ─────────────────────────────────
        if opcao == "1":
            try:
                id_    = repo_clientes.proximo_id()
                nome   = input("  Nome       : ").strip()
                cpf    = input("  CPF        : ").strip()
                tel    = input("  Telefone   : ").strip()
                email  = input("  E-mail     : ").strip()
                fid_i  = input("  Fidelidade (s/n): ").strip().lower()
                fid    = fid_i == "s"

                cliente = Cliente(id_, nome, cpf, tel, email, fid)
                repo_clientes.adicionar(cliente)
                print(f"  [OK] {cliente}")

            except CPFInvalidoError as e:
                print(f"  [ERRO] CPF inválido: {e}")
            except ValueError as e:
                print(f"  [ERRO] Dado inválido: {e}")
            except Exception as e:
                print(f"  [ERRO] Inesperado: {e}")

        # ── LISTAR CLIENTES ───────────────────────────────────
        elif opcao == "2":
            clientes = repo_clientes.listar_todos()
            if not clientes:
                print("  Nenhum cliente cadastrado.")
            for c in clientes:
                print(f"  {c}")

        # ── CADASTRAR PET ─────────────────────────────────────
        elif opcao == "3":
            try:
                id_cli_s = input("  ID do cliente: ").strip()
                id_cli   = int(id_cli_s)   # ValueError se não inteiro
                cliente  = repo_clientes.buscar_por_id(id_cli)
                if not cliente:
                    print("  [ERRO] Cliente não encontrado.")
                else:
                    id_  = repo_pets.proximo_id()
                    nome = input("  Nome do pet   : ").strip()
                    esp  = input("  Espécie (cão/gato/outro): ").strip().lower()
                    raca = input("  Raça          : ").strip()
                    prt  = input("  Porte (P/M/G) : ").strip().upper()
                    porte_map = {"P": PORTE_PEQUENO, "M": PORTE_MEDIO, "G": PORTE_GRANDE}
                    porte = porte_map.get(prt, PORTE_MEDIO)
                    idade = int(input("  Idade (anos)  : ").strip())
                    peso  = float(input("  Peso (kg)     : ").strip())

                    if esp == "cão":
                        pet = Cao(id_, nome, raca, porte, idade, peso, id_cli)
                    elif esp == "gato":
                        pet = Gato(id_, nome, raca, porte, idade, peso, id_cli)
                    else:
                        pet = Pet(id_, nome, esp, raca, porte, idade, peso, id_cli)

                    repo_pets.adicionar(pet)
                    cliente.adicionar_pet(nome)
                    print(f"  [OK] {pet}")

            except ValueError as e:
                print(f"  [ERRO] Dado inválido: {e}")
            except TypeError as e:
                print(f"  [ERRO] Tipo incorreto: {e}")
            except Exception as e:
                print(f"  [ERRO] Inesperado: {e}")

        # ── LISTAR PETS ───────────────────────────────────────
        elif opcao == "4":
            for p in repo_pets.listar_todos():
                print(f"  {p}")

        # ── NOVO AGENDAMENTO ──────────────────────────────────
        elif opcao == "5":
            try:
                id_cli = int(input("  ID do cliente : ").strip())
                id_pet = int(input("  ID do pet     : ").strip())
                cli    = repo_clientes.buscar_por_id(id_cli)
                pet    = repo_pets.buscar_por_id(id_pet)

                if not cli or not pet:
                    raise ValueError("Cliente ou pet não encontrado.")

                print(ServicoCalculadora.tabela_precos())
                srv  = input("  Nome do serviço (exato): ").strip()
                data = input("  Data (AAAA-MM-DD)       : ").strip()
                hora = input("  Hora (HH:MM)            : ").strip()

                calc = ServicoCalculadora.calcular(srv, cli.fidelidade)
                id_  = repo_agendamentos.proximo_id()
                ag   = Agendamento(
                    id_, cli.id, cli.nome, pet.id, pet.nome,
                    srv, data, hora,
                    calc["preco_base"], calc["valor_desconto"]
                )
                repo_agendamentos.adicionar(ag)
                print(f"  [OK] {ag}")

            except ValueError as e:
                print(f"  [ERRO]: {e}")
            except Exception as e:
                print(f"  [ERRO] Inesperado: {e}")

        # ── LISTAR AGENDAMENTOS ───────────────────────────────
        elif opcao == "6":
            for ag in repo_agendamentos.listar_todos():
                print(f"  {ag}")

        # ── ALTERAR STATUS ────────────────────────────────────
        elif opcao == "7":
            try:
                id_ag = int(input("  ID do agendamento: ").strip())
                ag    = repo_agendamentos.buscar_por_id(id_ag)
                if not ag:
                    raise ValueError("Agendamento não encontrado.")
                print(f"  Status atual: {ag.status}")
                print("  [1] Iniciar  [2] Concluir  [3] Cancelar")
                acao = input("  Ação: ").strip()
                if acao == "1":
                    ag.confirmar_inicio()
                elif acao == "2":
                    ag.concluir()
                elif acao == "3":
                    ag.cancelar()
                else:
                    raise ValueError("Ação inválida.")
                print(f"  [OK] Novo status: {ag.status}")

            except (ValueError, AgendamentoInvalidoError) as e:
                print(f"  [ERRO]: {e}")
            except Exception as e:
                print(f"  [ERRO] Inesperado: {e}")

        # ── RELATÓRIO TXT ─────────────────────────────────────
        elif opcao == "8":
            ok = gerar_relatorio_txt(repo_clientes, repo_pets, repo_agendamentos)
            if ok:
                print(f"  [OK] Relatório salvo em '{ARQ_RELATORIO}'.")

        # ── ENCERRAR ──────────────────────────────────────────
        elif opcao == "0":
            encerrar_sistema(repo_clientes, repo_pets, repo_agendamentos)
            break

        else:
            print("  [ERRO] Opção inválida.")


if __name__ == "__main__":
    main()