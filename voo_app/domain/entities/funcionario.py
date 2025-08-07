from domain.entities.pessoa import Pessoa
from datetime import datetime
from domain.interfaces.logavel import Logavel
from domain.mixins.identificavel import IndentificavelMixin

class Funcionario(Pessoa, Logavel, IndentificavelMixin):
    def __init__(self, nome:str, cpf:str, cargo:str, matricula:str):
        super().__init__(nome, cpf)
        self.cargo = cargo
        self.matricula = matricula

    def exibir_dados(self):
        return (
            f"Nome: {self.nome}\n"
            f"CPF: {self.cpf}\n"
            f"Cargo: {self.cargo}\n"
            f"Matrícula: {self.matricula}"
        )
    
    def logar_entrada(self, horario: datetime=None):
        if horario:
            horario = datetime.now()
        print(f"Funcionário: {self.nome} (Matrícula: {self.matricula}) logou no sistema às {horario}!")
