class Lancamentos():
    def __init__(self, data, valor, descricao, conta_corrente):
        self.data = data
        self.valor = valor
        self.descricao = descricao
        self.conta_corrente = conta_corrente

    def exibirGasto(self):
        print(f"Gasto realizado dia {self.data} no valor de {self.valor} referente a {self.descricao} na conta {self.conta_corrente} ")

todos_lancamentos = []