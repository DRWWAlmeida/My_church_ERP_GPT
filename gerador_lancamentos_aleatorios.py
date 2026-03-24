import random
from models import Lancamentos, ContaCorrente, todos_lancamentos, todas_contas_correntes

def cadastrar_automatico(quantidade):
    # Listas de opções para o sorteio
    descricoes = ["Mercado", "Farmácia", "Gasolina", "Restaurante", "Netflix", "Aluguel", "Academia"]
    contas = ["NuBank", "Inter", "Santander", "Itaú"]

    for conta in contas:
        nova_conta_corrente = ContaCorrente(conta)
        todas_contas_correntes.append(nova_conta_corrente)
    
    for _ in range(quantidade):
        # Gera data aleatória (exemplo para o ano de 2024)
        dia = random.randint(1, 28)
        mes = random.randint(1, 12)
        data_aleatoria = f"{dia:02d}/{mes:02d}/2025"
        
        # Gera valor entre 10.00 e 500.00
        valor_aleatorio = round(random.uniform(10.0, 500.0), 2)
        
        # Sorteia descrição e conta
        desc_aleatoria = random.choice(descricoes)
        conta_aleatoria = random.choice(todas_contas_correntes)
        
        # Cria o objeto e adiciona à lista global
        novo_lancamento = Lancamentos(data_aleatoria, str(valor_aleatorio), desc_aleatoria, conta_aleatoria)
        todos_lancamentos.append(novo_lancamento)
        
    print(f"{quantidade} lançamentos gerados com sucesso!")