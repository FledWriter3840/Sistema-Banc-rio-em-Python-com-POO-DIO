from abc import ABC, abstractproperty, classmethod, abstractmethod
from datetime import datetime
import textwrap

class Cliente:
    def __init__(self, endereco,):
        self.endereco = endereco
        self.contas = []
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)
    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, cpf, endereco, nome, data_nascimento):
        self.cpf = cpf
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento

class Conta:
    def __init__(self, numero,cliente):
        self._numero = numero
        self._cliente = cliente
        self._saldo = 0
        self._historico = Historico()
        self.agencia = "0001"
        @classmethod
        def nova_conta(cls, cliente, numero):
            return cls(numero, cliente)

        @property
        def saldo(self):
            return self._saldo
        @property
        def numero(self):
            return self._numero
        @property
        def cliente(self):
            return self._cliente
        @property
        def historico(self):
            return self._historico
        @property
        def agencia(self):
            return self._agencia
        def sacar(self, valor):
            saldo = self.saldo
            excedeu_saldo = valor > saldo
            if excedeu_saldo:
                print("Operação falhou! Você não tem saldo suficiente.")
            elif valor > 0:
                self._saldo -= valor
                print("Saque realizado com sucesso!")
                return True
            else:
                print("Operação falhou! O valor informado é inválido.")
            return False

        def depositar(self, valor):
            if valor > 0:
                self._saldo += valor
                print("Depósito realizado com sucesso!")
            else:
                print("Operação falhou! O valor informado é inválido.")
                return False
            return True

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limte_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len([transacao for transacao in self.historico.operacoes if transacao.__class__ == Saque])
        
        excedeu_limite_saques = numero_saques >= self.limte_saques
        
        excedeu_limite_valor = valor > self.limite
        
        if excedeu_limite_saques:
            print("Operação falhou! Número máximo de saques excedido.")
        elif excedeu_limite_valor:
            print("Operação falhou! O valor do saque excede o limite.")
        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        return f"Número: {self.numero}\nTitular: {self.cliente.nome}\nSaldo: {self.saldo}\nLimite: {self.limite}\nLimite de saques: {self.limte_saques}\nAgência: {self.agencia}"

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "data_hora": datetime.now(),
                "transacao": transacao,
                "valor": transacao.valor
            }
        )   

class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @classmethod
    def registrar(self, conta):
        pass
        
class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor
    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self._valor)
        
        if sucesso_transacao:
            self._historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor
    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self._valor)
        if sucesso_transacao:
            self._historico.adicionar_transacao(self)

def menu():
    menu = """\n
    [1] Depositar
    [2] Sacar
    [3] Extrato
    [4] Nova Conta
    [5] Listar Contas
    [6] Novo Usuário
    [7] Sair
    => """
    return input(textwrap.dedent(menu))

def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta(cliente):
    if not cliente.contas:
        print("O cliente não possui contas!")
        return
    return cliente.contas[0]

def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("Cliente não encontrado!")
        return
    
    valor = float(input("Informe o valor do depósito: "))

    transacao = Deposito(valor)
    
    conta = recuperar_conta(cliente)
    
    if not conta:
        print("Conta não encontrada!")
        return
    
    cliente.realizar_transacao(transacao)
    
def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("Cliente não encontrado!")
        return

    valor = float(input("Informe o valor do saque: "))

    transacao = Saque(valor)

    conta = recuperar_conta(cliente)

    if not conta:
        print("Conta não encontrada!")
        return

    cliente.realizar_transacao(transacao)

def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("Cliente não encontrado!")
        return

    conta = recuperar_conta(cliente)

    if not conta:
        print("Conta não encontrada!")
        return
    
    print("Extrato")
    
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"{transacao['tipo']}:\n"
            extrato += f"\tData: {transacao['data_hora']}\n"
            extrato += f"\tValor: {transacao['valor']}\n"
            extrato += "\n"
    
    print(extrato)
    print(f"Saldo: {conta.saldo:.2f}")

def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente número): ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("Já existe um cliente com esse CPF!")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o Endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(cpf=cpf, nome=nome, data_nascimento=data_nascimento, endereco=endereco)

    clientes.append(PessoaFisica(cpf=cpf, nome=nome, data_nascimento=data_nascimento, endereco=endereco))

    print("Cliente criado com sucesso!")

def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("Cliente não encontrado!")
        return

    conta = ContaCorrente.nova_conta(numero = numero_conta, cliente=cliente)
    contas.append(conta)
    cliente.contas.append(conta)

    print("Conta criada com sucesso!")

def listar_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(f"""\
            Agência:\t{conta.agencia}
            C/C:\t\t{conta.numero}
            Titular:\t{conta.cliente.nome})
        """))

def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "1":
            depositar(clientes)
        elif opcao == "2":
            sacar(clientes)
        elif opcao == "3":
            exibir_extrato(clientes)
        elif opcao == "4":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)
        elif opcao == "5":
            listar_contas(clientes)
        elif opcao == "6":
            criar_cliente(clientes)
        elif opcao == "7":
            break
        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")




