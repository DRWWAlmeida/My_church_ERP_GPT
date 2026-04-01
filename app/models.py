class Lancamentos():
    def __init__(self, data, valor, descricao, contas_correntes_id, tipo_lancamento_id, categorias_id):
        self.data = data
        self.valor = valor
        self.descricao = descricao
        self.conta_corrente_id = contas_correntes_id
        self.tipo_lancamento_id = tipo_lancamento_id
        self.categorias_id = categorias_id


    def exibirGasto(self):
        print(f"Gasto realizado dia {self.data} no valor de {self.valor} referente a {self.descricao} na conta {self.contas_correntes_id} ")

class ContaCorrente():
    def __init__(self, nome):
        self.nome = nome

    def exibirContas(self):
        print(self.nome)

class TipoLancamento():
    def __init__(self, nome):
        self.nome = nome

    def exibirTipoLancamento(self):
        print(self.nome)

class Categoria():
    def __init__(self, nome):
        self.nome = nome
    
    def exibirCategorias(self):
        print(self.nome)


todos_lancamentos = []
todas_contas_correntes = []