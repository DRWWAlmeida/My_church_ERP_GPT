from models import Lancamentos, todos_lancamentos
from gerador_lancamentos_aleatorios import cadastrar_automatico


def cadastrarLancamentos():
    data = input('Digita a data: ')
    valor = input("Digite o valor: ")
    descricao = input("Digite a descrição: ")
    conta_corrente = input("Digite a Conta Corrente: ")
    novo_lancamento = Lancamentos(data, valor, descricao, conta_corrente)
    todos_lancamentos.append(novo_lancamento)
    print("Lançamento gravado com sucesso!")

def listarGastos():
    for lancamento in todos_lancamentos:
        lancamento.exibirGasto()

def controler(opcao):
    match opcao:
        case "1":
            return cadastrarLancamentos()
        case "2":
            return listarGastos()
        case "0":
            return opcao

cadastrar_automatico(10)

while True:
    print("===============================")
    print("0.Sair")
    print("1. Cadastrar lançamento")
    print("2. Listar Lancamentos")
    print("Digite a opção selecionada: ")
    opcao = controler(input())
    if opcao == "0":
        print("Saindo do sistema...")
        break
