class Order:
    def __init__(self, disponivel, valor_bruto, taxa, valor_liquido, desconto_ant=0):
        self.disponivel = disponivel
        self.valor_bruto = valor_bruto
        self.taxa = taxa
        self.valor_liquido = valor_liquido
        self.desconto_ant = desconto_ant

    def __str__(self):
        return f'Disponível em: {self.disponivel}\tValor bruto: {self.valor_bruto}\tTaxa: {self.taxa}\tValor liquido:{self.valor_liquido}'
