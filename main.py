from models import Lancamentos, ContaCorrente, todos_lancamentos, todas_contas_correntes
from gerador_lancamentos_aleatorios import cadastrar_automatico


def cadastrarLancamentos():
    data = input('Digita a data: ')
    valor = input("Digite o valor: ")
    descricao = input("Digite a descrição: ")
    conta_corrente = input("Digite a Conta Corrente: ")
    novo_lancamento = Lancamentos(data, valor, descricao, conta_corrente)
    todos_lancamentos.append(novo_lancamento)
    print("Lançamento gravado com sucesso!")

def cadastrarContaCorrente():
    conta_corrente = input("Digite o nome da conta corrente: ")
    nova_conta_corrente = ContaCorrente(conta_corrente)
    todas_contas_correntes.append(nova_conta_corrente)

def listarGastos():
    for lancamento in todos_lancamentos:
        lancamento.exibirGasto()

def listarContasCorrentes():
    print(todas_contas_correntes)
    n = 1
    for conta in todas_contas_correntes:
        print(f'{n}. {conta.nome}')
        n += 1
        

def controler(opcao):
    match opcao:
        case "1":
            return cadastrarLancamentos()
        case "2":
            return listarGastos()
        case "3":
            return cadastrarContaCorrente()
        case "4":
            return listarContasCorrentes()
        case "0":
            return opcao

cadastrar_automatico(10)

while True:
    print("===============================")
    print("0. Sair")
    print("1. Cadastrar lançamento")
    print("2. Listar Lancamentos")
    print("3. Cadastrar Conta Corrente")
    print("4. Listar Contas Correntes")
    print("Digite a opção selecionada: ")
    opcao = controler(input())
    if opcao == "0":
        print("Saindo do sistema...")
        break
