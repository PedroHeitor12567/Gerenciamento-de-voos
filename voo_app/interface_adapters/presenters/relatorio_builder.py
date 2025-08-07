from rich.table import Table

class _RelatorioBuilder:
    def __init__(self, titulo):
        self.tabela = Table(title=titulo, show_lines=True)
    
    def adicionar_colunas(self, *colunas):
        for nome, estilo, formatacao in colunas:
            self.tabela.add_column(nome, style=estilo, justify=formatacao)
    
    def adicionar_linhas(self, *valores):
        self.tabela.add_row(*[str(v) for v in valores])

    def construir(self):
        return self.tabela