from voo_app.domain.entities.pessoa import Pessoa
from datetime import datetime
from voo_app.domain.interfaces.logavel import Logavel
from voo_app.domain.mixins.identificavel import IndentificavelMixin

class Funcionario(Pessoa, Logavel, IndentificavelMixin):
    """Classe que representa um funcionário do sistema.

    Herda de:
        Pessoa: Classe base com nome e CPF.
        Logavel: Interface que exige implementação do método de log.
        IndentificavelMixin: Mixin para gerar identificadores únicos.

    Attributes:
        cargo (str): Cargo ocupado pelo funcionário.
        matricula (str): Identificador único do funcionário dentro da empresa.
    """

    def __init__(self, nome: str, cpf: str, cargo: str, matricula: str):
        """Inicializa um funcionário com os dados fornecidos.

        Args:
            nome (str): Nome do funcionário.
            cpf (str): CPF do funcionário.
            cargo (str): Cargo exercido.
            matricula (str): Matrícula funcional do funcionário.
        """
        super().__init__(nome, cpf)
        self.cargo = cargo
        self.matricula = matricula

    def exibir_dados(self) -> str:
        """Exibe os dados do funcionário de forma formatada.

        Returns:
            str: Dados formatados do funcionário.
        """
        return (
            f"Nome: {self.nome}\n"
            f"CPF: {self.cpf}\n"
            f"Cargo: {self.cargo}\n"
            f"Matrícula: {self.matricula}"
        )
    
    def logar_entrada(self, horario: datetime = None):
        """Registra a entrada do funcionário no sistema.

        Args:
            horario (datetime, optional): Horário do login. Se None, será usado o horário atual.
        """
        if horario is None:
            horario = datetime.now()
        print(f"Funcionário: {self.nome} (Matrícula: {self.matricula}) logou no sistema às {horario}!")