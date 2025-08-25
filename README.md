# 🏦 Sistema Bancário em Python

Este projeto é uma simulação de **sistema bancário simples**, desenvolvido em Python, utilizando **Programação Orientada a Objetos (POO)**, boas práticas de modularização e princípios de abstração.

## 🔹 Funcionalidades

O sistema permite:

* Criar clientes (Pessoa Física).
* Criar contas bancárias (Conta Corrente).
* Realizar **depósitos** e **saques**.
* Exibir **extrato** com histórico de transações.
* Listar todas as contas cadastradas.

## 📂 Estrutura do Código

* **Cliente / PessoaFisica** → Representa os clientes do banco.
* **Conta / ContaCorrente** → Implementa a conta bancária com regras de limite e saques.
* **Transações (Depósito e Saque)** → São registradas no histórico da conta.
* **Histórico** → Armazena todas as movimentações realizadas.
* **Menu interativo** → Permite que o usuário interaja pelo terminal.

## 📖 Exemplo de uso

Ao executar, o menu interativo será exibido:

```
[1] Depositar
[2] Sacar
[3] Extrato
[4] Nova Conta
[5] Listar Contas
[6] Novo Usuário
[7] Sair
=> 
```

Basta selecionar a operação desejada e seguir as instruções no terminal.

## 🛠 Tecnologias utilizadas

* **Python 3**
* **ABC (Abstract Base Classes)** para abstração.
* **Datetime** para registro de data/hora das transações.
* **Textwrap** para formatação do menu.

## 🚀 Melhorias futuras

* Implementar persistência de dados (salvar em arquivos ou banco de dados).
* Criar interface gráfica (GUI) ou API para consumo via web.
* Suporte a diferentes tipos de contas (poupança, investimento etc.).
