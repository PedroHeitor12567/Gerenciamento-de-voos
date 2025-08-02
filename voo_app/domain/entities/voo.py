from typing import List
from domain.entities.passageiro import Passageiro
from domain.entities.funcionario import Funcionario
from domain.entities.mini_aeronave import MiniAeronave
class Voo:
    def __init__(self, numero_voo, origem, destino, aeronave):
        self.numero_voo = numero_voo
        self.origem = origem
        self.destino = destino
        self.aeronave = aeronave
        self.passageiros: list[Passageiro] = []
        self.tripulacao: list[Funcionario] = []
    
    def adicionar_passageiros():
        pass