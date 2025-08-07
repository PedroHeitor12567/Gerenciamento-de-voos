from domain.entities.passageiro import Passageiro
from domain.entities.funcionario import Funcionario
from domain.entities.mini_aeronave import MiniAeronave
from interface_adapters.presenters.relatorio_builder import _RelatorioBuilder
from infrastructure.database.models_method import listar_passageiros, listar_funcionarios
class Voo:
    def __init__(self, numero_voo, origem, destino, aeronave: MiniAeronave):
        self.numero_voo = numero_voo
        self.origem = origem
        self.destino = destino
        self.aeronave = aeronave
        self.passageiros: list[Passageiro] = []
        self.tripulacao: list[Funcionario] = []
    
    def adicionar_passageiros(self, passageiro: Passageiro):
        if passageiro in self.passageiros:
            print(f"Passageiro {passageiro.nome} já está no voo {self.numero_voo}.")
        elif len(self.passageiros) >= self.aeronave.capacidade:
            print(f"A aeronave está cheia. Não é possível adicionar o passageiro {passageiro.nome}.")
        else:
            self.passageiros.append(passageiro)
            print(f"Passageiro {passageiro.nome} adicionado ao voo {self.numero_voo}.")
    
    def adicionar_tripulante(self, tripulante: Funcionario):
        if tripulante in self.tripulacao:
            print(f"Tripulante {tripulante.nome} já está na tripulação do voo {self.numero_voo}.")
        else:
            self.tripulacao.append(tripulante)
            print(f"Tripulante {tripulante.nome} adicionado na tripulação do voo {self.numero_voo}.")

    def listar_passageiros(self):
        construindo = _RelatorioBuilder("Todos os Passageiros")
        construindo.adicionar_colunas(
            ("ID", "cyan", "center"),
            ("Nome", "yellow", "center"),
            ("CPF", "green", "center"),
            ("Bagagens", "white", "center")
        )

        rows = listar_passageiros()
        for row in rows:
            construindo.adicionar_linhas(
                row[0],
                row[1],
                row[2],
                row[3]
            )
        
        return construindo.construir()
    
    def listar_tripulacao(self):
        print(f"Tripulação do voo {self.numero_voo}:")
        if not self.tripulacao:
            print("Nenhum tripulante encontrado.")
        for tripulante in self.tripulacao:
            print(f"- {tripulante.nome} ({tripulante.cargo})")
        