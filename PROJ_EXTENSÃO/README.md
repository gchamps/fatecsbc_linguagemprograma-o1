# 🐾 Sistema AmigoPet – Gerenciamento de PetShop

> **Projeto de Extensão – Linguagem de Programação I**
> Desenvolvido pelos alunos: Gabriel Champin - Luana Monteiro - Luigi Matheus - Walter Augusto  
> Curso: Informática para Negócios | FATEC  
> Organização Parceira: PetShop AmigoPet Ltda.

---

## Introdução

O **Sistema AmigoPet** é um MVP (Mínimo Produto Viável) desenvolvido como projeto de extensão da disciplina de Linguagem de Programação I, com o objetivo de digitalizar e automatizar os processos operacionais do PetShop AmigoPet Ltda., empresa parceira localizada em São Paulo – SP.

O sistema foi desenvolvido em quatro fases evolutivas, cobrindo desde a estrutura de dados inicial até a implementação completa com Programação Orientada a Objetos e persistência em arquivos CSV e TXT.

---

## Problema Identificado

O PetShop AmigoPet operava inteiramente com fichas físicas e planilhas manuais, resultando em:

- Perda de informações de clientes e histórico de atendimentos
- Erros de precificação por cálculo manual
- Ausência de controle de agenda (overbooking frequente)
- Tempo excessivo de atendimento por falta de consulta rápida
- Impossibilidade de gerar relatórios gerenciais

---

## Solução Proposta

Sistema CLI (Command Line Interface) em Python com:

- Cadastro completo de clientes e pets
- Gerenciamento de agendamentos com controle de status
- Precificação automática com descontos e impostos
- Alertas automáticos de lotação e pendências
- Relatórios de faturamento e serviços populares
- Persistência automática em CSV e TXT

---

## Tecnologias Utilizadas

| Tecnologia | Versão | Finalidade |
|---|---|---|
| Python | 3.11+ | Linguagem principal |
| csv (stdlib) | — | Persistência em CSV |
| os (stdlib) | — | Manipulação de arquivos |
| datetime (stdlib) | — | Datas e horários |
| re (stdlib) | — | Validação de CPF |

---

## Requisitos

- Python 3.11 ou superior
- Nenhuma dependência externa (apenas biblioteca padrão)

---

## Instalação

```bash
# 1. Clone ou baixe o repositório
git clone https://github.com/gchamps/fatecsbc_linguagemprograma-o1/tree/main/PROJ_EXTENS%C3%83O
cd amigopet

# 2. (Opcional) Crie ambiente virtual
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows
```

---

## Execução

```bash
# Fase 1 – Estrutura de dados e cálculo
python fase1_estrutura.py

# Fase 2 – Sistema CLI completo (com dados de demonstração)
python fase2_cli.py

# Fase 3 – Demonstração de POO
python fase3_poo.py

# Fase 4 – Sistema completo com persistência (RECOMENDADO)
python fase4_persistencia.py
```

> **Importante:** Execute a partir da pasta `codigo/`. O sistema cria automaticamente a pasta `dados/` para os arquivos CSV e TXT.

---

## Estrutura do Projeto

```
amigopet/
├── codigo/
│   ├── fase1_estrutura.py       # Constantes, variáveis, tipos, cálculo de negócio
│   ├── fase2_cli.py             # Sistema CLI com CRUD, relatórios e alertas
│   ├── fase3_poo.py             # Classes, herança, encapsulamento, repositórios
│   └── fase4_persistencia.py   # Persistência CSV/TXT, exceções, startup/shutdown
├── dados/                       # Criado automaticamente pelo sistema
│   ├── clientes.csv
│   ├── pets.csv
│   ├── agendamentos.csv
│   ├── log_operacoes.txt
│   └── relatorio_diario.txt
├── docs/
│   └── projeto_extensao.docx   # Documento acadêmico completo
└── README.md
```

---

## Funcionalidades

### Clientes
- ✅ Cadastrar com validação de CPF (formato 000.000.000-00)
- ✅ Consultar por ID ou nome parcial
- ✅ Listar em tabela formatada
- ✅ Alterar dados (nome, telefone, e-mail, fidelidade)
- ✅ Excluir com verificação de agendamentos ativos

### Pets
- ✅ Cadastrar vinculado a cliente (cão, gato ou outro)
- ✅ Listar com filtro por cliente
- ✅ Registro de vacinas (classe Cao)
- ✅ Classificação por porte e ciclo de vida

### Agendamentos
- ✅ Criar com cálculo automático de preço
- ✅ Controle de ciclo de vida: Agendado → Em Andamento → Concluído
- ✅ Alerta de lotação de agenda (máximo 20/dia)
- ✅ Cancelamento com validação

### Precificação
- ✅ Desconto fidelidade (10%)
- ✅ Desconto combo (15%)
- ✅ ISS automático (5%)
- ✅ Regra: aplica o maior desconto aplicável

### Persistência
- ✅ Carregamento automático ao iniciar
- ✅ Salvamento automático ao encerrar
- ✅ Arquivo de log de operações (TXT)
- ✅ Relatório diário gerado em TXT

### Tratamento de Exceções
- ✅ `ValueError` – dados inválidos
- ✅ `TypeError` – tipos incorretos
- ✅ `FileNotFoundError` – primeira execução
- ✅ `Exception` – erros genéricos

---

## Exemplos de Uso

### Calcular preço de um serviço

```python
from fase1_estrutura import calcular_valor_servico, PRECO_BANHO_GRANDE

resultado = calcular_valor_servico(
    preco_base=90.00,
    fidelidade=True,
    combo=False
)
# {'valor_final': 85.05, 'valor_desconto': 9.0, 'valor_iss': 4.05, ...}
```

### Criar cliente e pet com POO

```python
from fase3_poo import Cliente, Cao, PORTE_GRANDE

cliente = Cliente(1, "Maria Oliveira", "111.222.333-44",
                   "(11) 98765-4321", "maria@email.com", fidelidade=True)

pet = Cao(1, "Thor", "Golden Retriever", PORTE_GRANDE, 3, 28.5, id_cliente=1)
pet.registrar_vacina("Antirrábica", "2025-03-10")

print(cliente)  # Cliente #1: Maria Oliveira | 111.222.333-44 ✓ Fidelidade
print(pet)      # Pet #1: Thor (Cão/Golden Retriever) | Grande | 3a | 28.5kg [Cão | 1 vacina(s)]
```

### Persistência

```python
from fase4_persistencia import inicializar_sistema, encerrar_sistema
from fase3_poo import RepositorioClientes, RepositorioPets, RepositorioAgendamentos

repo_cli = RepositorioClientes()
repo_pts = RepositorioPets()
repo_ag  = RepositorioAgendamentos()

inicializar_sistema(repo_cli, repo_pts, repo_ag)   # carrega do disco
# ... operações ...
encerrar_sistema(repo_cli, repo_pts, repo_ag)      # salva e gera relatório
```

---

## Melhorias Futuras

1. **Interface gráfica (Tkinter ou web)** – substituir o CLI por GUI
2. **Banco de dados relacional (SQLite/PostgreSQL)** – substituir CSV
3. **API REST** – expor funcionalidades via HTTP para app mobile
4. **Módulo financeiro** – contas a pagar/receber, fluxo de caixa
5. **Agenda visual** – calendário interativo de atendimentos
6. **Notificações automáticas** – lembretes por WhatsApp/e-mail
7. **Prontuário veterinário** – histórico clínico completo por pet
8. **Controle de estoque** – produtos e insumos do petshop
9. **Módulo de vendas** – PDV integrado ao sistema
10. **Relatórios gráficos** – dashboards com matplotlib/plotly

---

## Cronograma

| Semana | Fase | Atividade | Entregável |
|---|---|---|---|
| 1-2 | Planejamento | Diagnóstico e levantamento de requisitos | Documento de requisitos |
| 3 | Fase 1 | Estrutura de dados, constantes, cálculo | `fase1_estrutura.py` |
| 4-5 | Fase 2 | Sistema CLI com CRUD completo | `fase2_cli.py` |
| 6-7 | Fase 3 | Refatoração com POO | `fase3_poo.py` |
| 8-9 | Fase 4 | Persistência e tratamento de exceções | `fase4_persistencia.py` |
| 10 | Documentação | README, docstrings, projeto acadêmico | `README.md`, `.docx` |
| 11 | Testes | Validação com a organização parceira | Relatório de testes |
| 12 | Apresentação | Entrega final e demonstração | Projeto completo |

---

## Autores

- Gabriel Champin - Luana Monteiro - Luigi Matheus - Walter Augusto
- Projeto desenvolvido como parte do Projeto de Extensão da disciplina **Linguagem de Programação I**
- Curso: **Irformática para Negócios**
- Instituição: **FATEC – Adib Moisés Dib**
- Organização Parceira: **PetShop AmigoPet Ltda.**

---

## Licença

Este projeto foi desenvolvido exclusivamente para fins acadêmicos como parte de projeto de extensão universitária.