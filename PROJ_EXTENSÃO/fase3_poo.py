"""
=============================================================================
PROJETO DE EXTENSÃO – LINGUAGEM DE PROGRAMAÇÃO I
Disciplina: Linguagem de Programação I | Curso: ADS | FATEC
Organização Parceira: PetShop AmigoPet Ltda.
Fase 3: Programação Orientada a Objetos (POO)
=============================================================================
Descrição:
    Refatoração completa do sistema utilizando POO com:
      • Encapsulamento (atributos privados com _ e __)
      • Getters e Setters (properties Python)
      • Validações no construtor e nos setters
      • Métodos de negócio coesos nas classes
      • Herança entre Pet e suas especializações
      • Classe repositório para gerenciar coleções

Diagrama de Classes (notação textual UML):
─────────────────────────────────────────────────────────────────────────────
┌─────────────────────┐       ┌──────────────────────────┐
│      Cliente        │1    *│         Pet               │
├─────────────────────┤◄──────├──────────────────────────┤
│ -__id: int          │       │ -__id: int                │
│ -__nome: str        │       │ -__nome: str              │
│ -__cpf: str         │       │ -__especie: str           │
│ -__telefone: str    │       │ -__raca: str              │
│ -__email: str       │       │ -__porte: str             │
│ -__fidelidade: bool │       │ -__idade: int             │
│ -__pets: list       │       │ -__peso_kg: float         │
├─────────────────────┤       │ -__id_cliente: int        │
│ +id: property       │       ├──────────────────────────┤
│ +nome: property     │       │ +id: property             │
│ +cpf: property      │       │ +nome: property           │
│ +fidelidade: bool   │       │ +porte: property          │
├─────────────────────┤       │ +peso_kg: property        │
│ +adicionar_pet()    │       ├──────────────────────────┤
│ +to_dict()          │       │ +to_dict()                │
│ +__str__()          │       │ +__str__()                │
└─────────────────────┘       └──────────────────────────┘
                                        △
                           ┌────────────┴─────────────┐
                    ┌──────┴──────┐           ┌────────┴──────┐
                    │    Cao      │           │    Gato       │
                    ├─────────────┤           ├───────────────┤
                    │ -__rastreio │           │ -__indoor     │
                    ├─────────────┤           ├───────────────┤
                    │+registrar() │           │+descricao()   │
                    └─────────────┘           └───────────────┘

┌────────────────────────────────────────────────┐
│                 Agendamento                    │
├────────────────────────────────────────────────┤
│ -__id: int                                     │
│ -__id_cliente: int                             │
│ -__id_pet: int                                 │
│ -__servico: str                                │
│ -__data: str                                   │
│ -__hora: str                                   │
│ -__status: str                                 │
│ -__valor_bruto: float                          │
│ -__valor_final: float                          │
├────────────────────────────────────────────────┤
│ +calcular_valor(): dict                        │
│ +confirmar() / concluir() / cancelar()         │
│ +to_dict(): dict                               │
└────────────────────────────────────────────────┘

┌─────────────────────┐   ┌─────────────────────┐   ┌──────────────────────┐
│ Repositorio<T>      │   │ RepositorioClientes  │   │ RepositorioPets      │
├─────────────────────┤   ├─────────────────────┤   ├──────────────────────┤
│ -__registros: list  │   │ +buscar_cpf()        │   │ +listar_por_cliente()│
├─────────────────────┤   └─────────────────────┘   └──────────────────────┘
│ +adicionar()        │
│ +buscar_por_id()    │   ┌────────────────────────────┐
│ +listar_todos()     │   │  ServicoCalculadora        │
│ +remover_por_id()   │   ├────────────────────────────┤
│ +__len__()          │   │ (métodos estáticos)        │
└─────────────────────┘   ├────────────────────────────┤
                          │ +calcular_valor_servico()  │
                          │ +tabela_precos()            │
                          └────────────────────────────┘
─────────────────────────────────────────────────────────────────────────────

Autor: Projeto Extensão – Turma ADS 2025
Data: 2025
=============================================================================
"""

import re
import datetime
from fase1_estrutura import (
    calcular_valor_servico,
    PRECO_BANHO_PEQUENO, PRECO_BANHO_MEDIO, PRECO_BANHO_GRANDE,
    PRECO_TOSA_SIMPLES, PRECO_TOSA_COMPLETA,
    PRECO_CONSULTA_VETERINARIA, PRECO_VACINA, PRECO_HOSPEDAGEM_DIARIA,
    STATUS_AGENDADO, STATUS_EM_ANDAMENTO, STATUS_CONCLUIDO, STATUS_CANCELADO,
    PORTE_PEQUENO, PORTE_MEDIO, PORTE_GRANDE,
)


# ============================================================
# EXCEÇÕES CUSTOMIZADAS DO DOMÍNIO
# ============================================================

class CPFInvalidoError(ValueError):
    """Levantada quando um CPF não passa na validação de formato."""
    pass


class AgendamentoInvalidoError(ValueError):
    """Levantada quando um agendamento possui estado inválido."""
    pass


class RegistroNaoEncontradoError(LookupError):
    """Levantada quando um registro não é encontrado pelo ID."""
    pass


# ============================================================
# CLASSE: Cliente
# ============================================================

class Cliente:
    """
    Representa um cliente do petshop.

    Encapsulamento:
        Todos os atributos são privados (prefixo __).
        O acesso externo ocorre exclusivamente via @property.

    Validações:
        - nome: não pode ser vazio
        - cpf: deve ter formato 000.000.000-00
        - telefone: não pode ser vazio
        - email: deve conter @
    """

    def __init__(self, id_: int, nome: str, cpf: str,
                 telefone: str, email: str, fidelidade: bool = False) -> None:
        # Atributos privados (name-mangling Python: __ → _Cliente__)
        self.__id          = id_
        self.nome      = nome          # usa o setter para validação
        self.cpf       = cpf
        self.telefone  = telefone
        self.email     = email
        self.__fidelidade  = bool(fidelidade)
        self.__pets        = []        # lista privada de nomes dos pets
        self.__data_cad    = datetime.date.today().isoformat()

    # ── GETTERS (read-only) ──────────────────────────────────
    @property
    def id(self) -> int:
        return self.__id

    @property
    def data_cad(self) -> str:
        return self.__data_cad

    @property
    def pets(self) -> list:
        return list(self.__pets)   # retorna cópia para proteger a lista interna

    # ── GETTER + SETTER: nome ────────────────────────────────
    @property
    def nome(self) -> str:
        return self.__nome

    @nome.setter
    def nome(self, valor: str) -> None:
        valor = str(valor).strip()
        if not valor:
            raise ValueError("Nome do cliente não pode ser vazio.")
        if len(valor) < 3:
            raise ValueError("Nome deve ter pelo menos 3 caracteres.")
        self.__nome = valor

    # ── GETTER + SETTER: cpf ─────────────────────────────────
    @property
    def cpf(self) -> str:
        return self.__cpf

    @cpf.setter
    def cpf(self, valor: str) -> None:
        valor = str(valor).strip()
        padrao = re.compile(r"^\d{3}\.\d{3}\.\d{3}-\d{2}$")
        if not padrao.match(valor):
            raise CPFInvalidoError(
                f"CPF '{valor}' inválido. Use o formato 000.000.000-00."
            )
        self.__cpf = valor

    # ── GETTER + SETTER: telefone ────────────────────────────
    @property
    def telefone(self) -> str:
        return self.__telefone

    @telefone.setter
    def telefone(self, valor: str) -> None:
        valor = str(valor).strip()
        if not valor:
            raise ValueError("Telefone não pode ser vazio.")
        self.__telefone = valor

    # ── GETTER + SETTER: email ───────────────────────────────
    @property
    def email(self) -> str:
        return self.__email

    @email.setter
    def email(self, valor: str) -> None:
        valor = str(valor).strip()
        if valor and "@" not in valor:
            raise ValueError(f"E-mail '{valor}' inválido.")
        self.__email = valor

    # ── GETTER + SETTER: fidelidade ──────────────────────────
    @property
    def fidelidade(self) -> bool:
        return self.__fidelidade

    @fidelidade.setter
    def fidelidade(self, valor: bool) -> None:
        self.__fidelidade = bool(valor)

    # ── MÉTODOS DE NEGÓCIO ───────────────────────────────────
    def adicionar_pet(self, nome_pet: str) -> None:
        """Associa um pet a este cliente."""
        if nome_pet not in self.__pets:
            self.__pets.append(nome_pet)

    def remover_pet(self, nome_pet: str) -> None:
        """Remove um pet da lista do cliente."""
        if nome_pet in self.__pets:
            self.__pets.remove(nome_pet)

    def tem_fidelidade(self) -> bool:
        """Retorna True se o cliente está no programa de fidelidade."""
        return self.__fidelidade

    # ── SERIALIZAÇÃO ─────────────────────────────────────────
    def to_dict(self) -> dict:
        """Converte o objeto para dicionário (para persistência)."""
        return {
            "id"        : self.__id,
            "nome"      : self.__nome,
            "cpf"       : self.__cpf,
            "telefone"  : self.__telefone,
            "email"     : self.__email,
            "fidelidade": self.__fidelidade,
            "pets"      : self.__pets,
            "data_cad"  : self.__data_cad,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Cliente":
        """Reconstrói um objeto Cliente a partir de um dicionário."""
        c = cls(d["id"], d["nome"], d["cpf"],
                d["telefone"], d["email"], d.get("fidelidade", False))
        c.__dict__["_Cliente__pets"]     = d.get("pets", [])
        c.__dict__["_Cliente__data_cad"] = d.get("data_cad", "")
        return c

    def __str__(self) -> str:
        fid = "✓ Fidelidade" if self.__fidelidade else ""
        return f"Cliente #{self.__id}: {self.__nome} | {self.__cpf} {fid}"

    def __repr__(self) -> str:
        return f"Cliente(id={self.__id}, nome='{self.__nome}')"


# ============================================================
# CLASSE BASE: Pet
# ============================================================

class Pet:
    """
    Classe base para animais de estimação.

    Encapsula os atributos comuns de qualquer espécie de pet.
    Subclasses (Cao, Gato) adicionam comportamentos específicos.
    """

    PORTES_VALIDOS = (PORTE_PEQUENO, PORTE_MEDIO, PORTE_GRANDE)

    def __init__(self, id_: int, nome: str, especie: str, raca: str,
                 porte: str, idade: int, peso_kg: float, id_cliente: int) -> None:
        self.__id         = id_
        self.nome         = nome
        self.__especie    = str(especie).strip().capitalize()
        self.raca         = raca
        self.porte        = porte
        self.idade        = idade
        self.peso_kg      = peso_kg
        self.__id_cliente = id_cliente

    # ── GETTERS READ-ONLY ────────────────────────────────────
    @property
    def id(self) -> int:
        return self.__id

    @property
    def especie(self) -> str:
        return self.__especie

    @property
    def id_cliente(self) -> int:
        return self.__id_cliente

    # ── GETTER + SETTER: nome ────────────────────────────────
    @property
    def nome(self) -> str:
        return self.__nome

    @nome.setter
    def nome(self, valor: str) -> None:
        valor = str(valor).strip()
        if not valor:
            raise ValueError("Nome do pet não pode ser vazio.")
        self.__nome = valor

    # ── GETTER + SETTER: raca ────────────────────────────────
    @property
    def raca(self) -> str:
        return self.__raca

    @raca.setter
    def raca(self, valor: str) -> None:
        self.__raca = str(valor).strip() or "SRD"

    # ── GETTER + SETTER: porte ───────────────────────────────
    @property
    def porte(self) -> str:
        return self.__porte

    @porte.setter
    def porte(self, valor: str) -> None:
        if valor not in self.PORTES_VALIDOS:
            raise ValueError(
                f"Porte '{valor}' inválido. Use: {self.PORTES_VALIDOS}"
            )
        self.__porte = valor

    # ── GETTER + SETTER: idade ───────────────────────────────
    @property
    def idade(self) -> int:
        return self.__idade

    @idade.setter
    def idade(self, valor: int) -> None:
        valor = int(valor)
        if valor < 0 or valor > 30:
            raise ValueError("Idade deve estar entre 0 e 30 anos.")
        self.__idade = valor

    # ── GETTER + SETTER: peso_kg ─────────────────────────────
    @property
    def peso_kg(self) -> float:
        return self.__peso_kg

    @peso_kg.setter
    def peso_kg(self, valor: float) -> None:
        valor = float(valor)
        if valor <= 0 or valor > 200:
            raise ValueError("Peso deve estar entre 0 e 200 kg.")
        self.__peso_kg = valor

    # ── MÉTODO DE NEGÓCIO ────────────────────────────────────
    def calcular_preco_banho(self) -> float:
        """Retorna o preço de banho de acordo com o porte do pet."""
        if self.__porte == PORTE_PEQUENO:
            return PRECO_BANHO_PEQUENO
        elif self.__porte == PORTE_MEDIO:
            return PRECO_BANHO_MEDIO
        else:
            return PRECO_BANHO_GRANDE

    def classificar_idade(self) -> str:
        """Classifica o pet como filhote, adulto ou idoso."""
        if self.__idade <= 1:
            return "Filhote"
        elif self.__idade <= 7:
            return "Adulto"
        else:
            return "Idoso"

    # ── SERIALIZAÇÃO ─────────────────────────────────────────
    def to_dict(self) -> dict:
        return {
            "id"         : self.__id,
            "nome"       : self.__nome,
            "especie"    : self.__especie,
            "raca"       : self.__raca,
            "porte"      : self.__porte,
            "idade"      : self.__idade,
            "peso_kg"    : self.__peso_kg,
            "id_cliente" : self.__id_cliente,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Pet":
        return cls(
            d["id"], d["nome"], d["especie"], d["raca"],
            d["porte"], d["idade"], d["peso_kg"], d["id_cliente"]
        )

    def __str__(self) -> str:
        return (f"Pet #{self.__id}: {self.__nome} ({self.__especie}/{self.__raca}) "
                f"| {self.__porte} | {self.__idade}a | {self.__peso_kg}kg")

    def __repr__(self) -> str:
        return f"Pet(id={self.__id}, nome='{self.__nome}', especie='{self.__especie}')"


# ============================================================
# SUBCLASSE: Cao (herda de Pet)
# ============================================================

class Cao(Pet):
    """
    Subclasse especializada para cães.
    Adiciona atributo de rastreamento de vacinas.
    """

    def __init__(self, id_: int, nome: str, raca: str, porte: str,
                 idade: int, peso_kg: float, id_cliente: int,
                 rastreio_vacinal: bool = False) -> None:
        super().__init__(id_, nome, "Cão", raca, porte, idade, peso_kg, id_cliente)
        self.__rastreio_vacinal = rastreio_vacinal
        self.__vacinas_aplicadas = []

    @property
    def rastreio_vacinal(self) -> bool:
        return self.__rastreio_vacinal

    def registrar_vacina(self, nome_vacina: str, data: str) -> None:
        """Registra uma vacina aplicada no cão."""
        self.__vacinas_aplicadas.append({
            "vacina": nome_vacina,
            "data"  : data,
        })

    def listar_vacinas(self) -> list:
        return list(self.__vacinas_aplicadas)

    def to_dict(self) -> dict:
        d = super().to_dict()
        d["rastreio_vacinal"]  = self.__rastreio_vacinal
        d["vacinas_aplicadas"] = self.__vacinas_aplicadas
        return d

    def __str__(self) -> str:
        base = super().__str__()
        vacinas = len(self.__vacinas_aplicadas)
        return f"{base} [Cão | {vacinas} vacina(s) registrada(s)]"


# ============================================================
# SUBCLASSE: Gato (herda de Pet)
# ============================================================

class Gato(Pet):
    """
    Subclasse especializada para gatos.
    Adiciona atributo de indoor/outdoor.
    """

    def __init__(self, id_: int, nome: str, raca: str, porte: str,
                 idade: int, peso_kg: float, id_cliente: int,
                 indoor: bool = True) -> None:
        super().__init__(id_, nome, "Gato", raca, porte, idade, peso_kg, id_cliente)
        self.__indoor = indoor

    @property
    def indoor(self) -> bool:
        return self.__indoor

    @indoor.setter
    def indoor(self, valor: bool) -> None:
        self.__indoor = bool(valor)

    def descricao_ambiente(self) -> str:
        """Descreve o ambiente de vida do gato."""
        return "Vive em ambiente interno" if self.__indoor else "Tem acesso externo"

    def to_dict(self) -> dict:
        d = super().to_dict()
        d["indoor"] = self.__indoor
        return d

    def __str__(self) -> str:
        base = super().__str__()
        amb  = "Indoor" if self.__indoor else "Outdoor"
        return f"{base} [Gato | {amb}]"


# ============================================================
# CLASSE: Agendamento
# ============================================================

class Agendamento:
    """
    Representa um agendamento de serviço no petshop.

    Controla o ciclo de vida do atendimento:
        Agendado → Em Andamento → Concluído
                ↘→ Cancelado
    """

    TRANSICOES_VALIDAS = {
        STATUS_AGENDADO      : (STATUS_EM_ANDAMENTO, STATUS_CANCELADO),
        STATUS_EM_ANDAMENTO  : (STATUS_CONCLUIDO, STATUS_CANCELADO),
        STATUS_CONCLUIDO     : (),
        STATUS_CANCELADO     : (),
    }

    def __init__(self, id_: int, id_cliente: int, nome_cliente: str,
                 id_pet: int, nome_pet: str, servico: str,
                 data: str, hora: str, valor_bruto: float,
                 desconto: float = 0.0) -> None:
        self.__id           = id_
        self.__id_cliente   = id_cliente
        self.__nome_cliente = nome_cliente
        self.__id_pet       = id_pet
        self.__nome_pet     = nome_pet
        self.servico        = servico
        self.data           = data
        self.hora           = hora
        self.__status       = STATUS_AGENDADO
        self.__valor_bruto  = float(valor_bruto)
        self.__desconto     = float(desconto)
        self.__valor_final  = round(self.__valor_bruto - self.__desconto, 2)
        self.__observacoes  = ""

    # ── GETTERS READ-ONLY ────────────────────────────────────
    @property
    def id(self) -> int:
        return self.__id

    @property
    def id_cliente(self) -> int:
        return self.__id_cliente

    @property
    def nome_cliente(self) -> str:
        return self.__nome_cliente

    @property
    def id_pet(self) -> int:
        return self.__id_pet

    @property
    def nome_pet(self) -> str:
        return self.__nome_pet

    @property
    def status(self) -> str:
        return self.__status

    @property
    def valor_bruto(self) -> float:
        return self.__valor_bruto

    @property
    def valor_final(self) -> float:
        return self.__valor_final

    @property
    def desconto(self) -> float:
        return self.__desconto

    # ── GETTER + SETTER: servico ─────────────────────────────
    @property
    def servico(self) -> str:
        return self.__servico

    @servico.setter
    def servico(self, valor: str) -> None:
        valor = str(valor).strip()
        if not valor:
            raise ValueError("Serviço não pode ser vazio.")
        self.__servico = valor

    # ── GETTER + SETTER: data ────────────────────────────────
    @property
    def data(self) -> str:
        return self.__data

    @data.setter
    def data(self, valor: str) -> None:
        # Valida formato AAAA-MM-DD
        try:
            datetime.date.fromisoformat(str(valor))
        except ValueError:
            raise ValueError(f"Data '{valor}' inválida. Use AAAA-MM-DD.")
        self.__data = str(valor)

    # ── GETTER + SETTER: hora ────────────────────────────────
    @property
    def hora(self) -> str:
        return self.__hora

    @hora.setter
    def hora(self, valor: str) -> None:
        partes = str(valor).split(":")
        if len(partes) != 2 or not all(p.isdigit() for p in partes):
            raise ValueError(f"Hora '{valor}' inválida. Use HH:MM.")
        self.__hora = valor

    # ── GETTER + SETTER: observacoes ─────────────────────────
    @property
    def observacoes(self) -> str:
        return self.__observacoes

    @observacoes.setter
    def observacoes(self, valor: str) -> None:
        self.__observacoes = str(valor).strip()

    # ── MÉTODOS DE CICLO DE VIDA ─────────────────────────────
    def _transicionar_status(self, novo_status: str) -> None:
        """Realiza transição de status com validação de fluxo."""
        permitidos = self.TRANSICOES_VALIDAS.get(self.__status, ())
        if novo_status not in permitidos:
            raise AgendamentoInvalidoError(
                f"Transição inválida: '{self.__status}' → '{novo_status}'. "
                f"Permitidas: {permitidos}"
            )
        self.__status = novo_status

    def confirmar_inicio(self) -> None:
        """Inicia o atendimento (Agendado → Em Andamento)."""
        self._transicionar_status(STATUS_EM_ANDAMENTO)

    def concluir(self) -> None:
        """Conclui o atendimento (Em Andamento → Concluído)."""
        self._transicionar_status(STATUS_CONCLUIDO)

    def cancelar(self) -> None:
        """Cancela o agendamento."""
        self._transicionar_status(STATUS_CANCELADO)

    def esta_ativo(self) -> bool:
        """Verifica se o agendamento está ativo (não concluído nem cancelado)."""
        return self.__status in (STATUS_AGENDADO, STATUS_EM_ANDAMENTO)

    # ── SERIALIZAÇÃO ─────────────────────────────────────────
    def to_dict(self) -> dict:
        return {
            "id"          : self.__id,
            "id_cliente"  : self.__id_cliente,
            "nome_cliente": self.__nome_cliente,
            "id_pet"      : self.__id_pet,
            "nome_pet"    : self.__nome_pet,
            "servico"     : self.__servico,
            "data"        : self.__data,
            "hora"        : self.__hora,
            "status"      : self.__status,
            "valor_bruto" : self.__valor_bruto,
            "valor_final" : self.__valor_final,
            "desconto"    : self.__desconto,
            "observacoes" : self.__observacoes,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Agendamento":
        ag = cls(
            d["id"], d["id_cliente"], d["nome_cliente"],
            d["id_pet"], d["nome_pet"], d["servico"],
            d["data"], d["hora"], d["valor_bruto"], d.get("desconto", 0.0)
        )
        ag.__dict__["_Agendamento__status"]      = d.get("status", STATUS_AGENDADO)
        ag.__dict__["_Agendamento__valor_final"] = d.get("valor_final", ag.valor_final)
        ag.__dict__["_Agendamento__observacoes"] = d.get("observacoes", "")
        return ag

    def __str__(self) -> str:
        return (f"Agendamento #{self.__id}: {self.__servico} | "
                f"{self.__nome_pet} ({self.__nome_cliente}) | "
                f"{self.__data} {self.__hora} | {self.__status} | "
                f"R$ {self.__valor_final:.2f}")

    def __repr__(self) -> str:
        return f"Agendamento(id={self.__id}, status='{self.__status}')"


# ============================================================
# CLASSE GENÉRICA: Repositorio<T>
# ============================================================

class Repositorio:
    """
    Repositório genérico para gerenciar coleções de objetos.

    Encapsula operações CRUD sobre uma lista de objetos que
    possuam atributo 'id' e método 'to_dict()'.
    """

    def __init__(self, nome: str) -> None:
        self.__nome      = nome
        self.__registros = []   # lista privada de objetos

    @property
    def nome(self) -> str:
        return self.__nome

    def adicionar(self, obj) -> None:
        """Adiciona um objeto ao repositório."""
        self.__registros.append(obj)

    def buscar_por_id(self, id_: int):
        """Busca e retorna um objeto pelo ID, ou None."""
        for obj in self.__registros:
            if obj.id == id_:
                return obj
        return None

    def listar_todos(self) -> list:
        """Retorna cópia da lista de todos os objetos."""
        return list(self.__registros)

    def remover_por_id(self, id_: int) -> bool:
        """Remove um objeto pelo ID. Retorna True se removido."""
        obj = self.buscar_por_id(id_)
        if obj:
            self.__registros.remove(obj)
            return True
        return False

    def proximo_id(self) -> int:
        """Gera o próximo ID sequencial."""
        if not self.__registros:
            return 1
        return max(obj.id for obj in self.__registros) + 1

    def to_list_dict(self) -> list:
        """Serializa todos os objetos como lista de dicionários."""
        return [obj.to_dict() for obj in self.__registros]

    def __len__(self) -> int:
        return len(self.__registros)

    def __repr__(self) -> str:
        return f"Repositorio(nome='{self.__nome}', total={len(self)})"


# ============================================================
# SUBCLASSES DE REPOSITÓRIO (especializações)
# ============================================================

class RepositorioClientes(Repositorio):
    """Repositório especializado para clientes."""

    def __init__(self) -> None:
        super().__init__("Clientes")

    def buscar_por_cpf(self, cpf: str) -> "Cliente | None":
        """Busca um cliente pelo CPF."""
        for c in self.listar_todos():
            if c.cpf == cpf:
                return c
        return None

    def buscar_por_nome(self, termo: str) -> list:
        """Busca clientes cujo nome contém o termo (case-insensitive)."""
        return [c for c in self.listar_todos()
                if termo.lower() in c.nome.lower()]


class RepositorioPets(Repositorio):
    """Repositório especializado para pets."""

    def __init__(self) -> None:
        super().__init__("Pets")

    def listar_por_cliente(self, id_cliente: int) -> list:
        """Retorna todos os pets de um cliente específico."""
        return [p for p in self.listar_todos()
                if p.id_cliente == id_cliente]


class RepositorioAgendamentos(Repositorio):
    """Repositório especializado para agendamentos."""

    def __init__(self) -> None:
        super().__init__("Agendamentos")

    def listar_por_data(self, data: str) -> list:
        """Retorna agendamentos de uma data específica."""
        return [ag for ag in self.listar_todos() if ag.data == data]

    def listar_ativos(self) -> list:
        """Retorna apenas agendamentos não finalizados."""
        return [ag for ag in self.listar_todos() if ag.esta_ativo()]

    def faturamento_total(self) -> float:
        """Calcula o faturamento total de serviços concluídos."""
        return sum(
            ag.valor_final for ag in self.listar_todos()
            if ag.status == STATUS_CONCLUIDO
        )


# ============================================================
# CLASSE UTILITÁRIA: ServicoCalculadora
# ============================================================

class ServicoCalculadora:
    """
    Classe utilitária com métodos estáticos para cálculo de preços.
    Não possui estado; todos os métodos são @staticmethod.
    """

    TABELA_SERVICOS = {
        "Banho Pequeno"       : PRECO_BANHO_PEQUENO,
        "Banho Médio"         : PRECO_BANHO_MEDIO,
        "Banho Grande"        : PRECO_BANHO_GRANDE,
        "Tosa Simples"        : PRECO_TOSA_SIMPLES,
        "Tosa Completa"       : PRECO_TOSA_COMPLETA,
        "Consulta Veterinária": PRECO_CONSULTA_VETERINARIA,
        "Vacina"              : PRECO_VACINA,
        "Hospedagem (diária)" : PRECO_HOSPEDAGEM_DIARIA,
    }

    @staticmethod
    def calcular(nome_servico: str, fidelidade: bool,
                  combo: bool = False) -> dict:
        """Calcula preço final de um serviço pelo nome."""
        preco = ServicoCalculadora.TABELA_SERVICOS.get(nome_servico)
        if preco is None:
            raise ValueError(f"Serviço '{nome_servico}' não encontrado.")
        return calcular_valor_servico(preco, fidelidade, combo)

    @staticmethod
    def tabela_precos() -> str:
        """Retorna string formatada com a tabela de preços."""
        linhas = ["=" * 45, f"{'TABELA DE PREÇOS':^45}", "=" * 45]
        for nome, preco in ServicoCalculadora.TABELA_SERVICOS.items():
            linhas.append(f"  {nome:<30} R$ {preco:>7.2f}")
        linhas.append("=" * 45)
        return "\n".join(linhas)


# ============================================================
# DEMONSTRAÇÃO DA FASE 3
# ============================================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("   FASE 3 – PROGRAMAÇÃO ORIENTADA A OBJETOS")
    print("   PetShop AmigoPet – Sistema de Gerenciamento")
    print("=" * 60)

    # Instancia repositórios
    repo_clientes    = RepositorioClientes()
    repo_pets        = RepositorioPets()
    repo_agendamentos = RepositorioAgendamentos()

    # Cria e adiciona clientes
    print("\n[1] Criando clientes...")
    c1 = Cliente(1, "Maria Oliveira", "111.222.333-44",
                  "(11) 98765-4321", "maria@email.com", fidelidade=True)
    c2 = Cliente(2, "João Santos", "555.666.777-88",
                  "(11) 91234-5678", "joao@email.com")
    repo_clientes.adicionar(c1)
    repo_clientes.adicionar(c2)
    print(c1)
    print(c2)

    # Cria e adiciona pets
    print("\n[2] Criando pets...")
    p1 = Cao(1, "Thor", "Golden Retriever", PORTE_GRANDE, 3, 28.5, 1)
    p1.registrar_vacina("Antirrábica", "2025-03-10")
    p2 = Gato(2, "Mel", "Siamês", PORTE_MEDIO, 4, 4.5, 2, indoor=True)
    repo_pets.adicionar(p1)
    repo_pets.adicionar(p2)
    print(p1)
    print(p2)
    print(f"  Vacinas do Thor: {p1.listar_vacinas()}")
    print(f"  Mel: {p2.descricao_ambiente()}")

    # Cria agendamento com ciclo de vida
    print("\n[3] Criando agendamento e testando ciclo de vida...")
    calc = ServicoCalculadora.calcular("Banho Grande", fidelidade=True)
    ag1 = Agendamento(
        1, c1.id, c1.nome, p1.id, p1.nome,
        "Banho Grande", "2025-08-20", "09:00",
        calc["preco_base"], calc["valor_desconto"]
    )
    print(f"  Criado: {ag1}")
    ag1.confirmar_inicio()
    print(f"  Após início: {ag1.status}")
    ag1.concluir()
    print(f"  Após conclusão: {ag1.status}")

    repo_agendamentos.adicionar(ag1)

    # Tentativa de transição inválida
    print("\n[4] Testando transição inválida...")
    try:
        ag1.cancelar()
    except AgendamentoInvalidoError as e:
        print(f"  [OK] Exceção capturada: {e}")

    # Validação de CPF inválido
    print("\n[5] Testando validação de CPF...")
    try:
        c_invalido = Cliente(99, "Teste", "cpf-invalido",
                              "(11) 9999-9999", "teste@email.com")
    except CPFInvalidoError as e:
        print(f"  [OK] Exceção capturada: {e}")

    # Faturamento total
    print(f"\n[6] Faturamento total (concluídos): R$ {repo_agendamentos.faturamento_total():.2f}")

    # Tabela de preços
    print(f"\n[7] Tabela de Preços:\n{ServicoCalculadora.tabela_precos()}")

    # Serialização
    print("\n[8] Serialização para dicionário:")
    print(f"  {c1.to_dict()}")