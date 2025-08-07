from voo_app.domain.entities.pessoa import Pessoa
from voo_app.domain.entities.bagagem import Bagagem

class Passageiro(Pessoa):
    """Classe que representa um passageiro, herda de Pessoa e possui bagagens associadas.

    Attributes:
        bagagens (list[Bagagem]): Lista de objetos Bagagem do passageiro.
    """

    def __init__(self, nome: str, cpf: str, bagagens: list[Bagagem] = None):
        """Inicializa um passageiro com nome, CPF e uma lista opcional de bagagens.

        Args:
            nome (str): Nome do passageiro.
            cpf (str): CPF do passageiro.
            bagagens (list[Bagagem], optional): Lista de bagagens do passageiro. 
                Caso não seja fornecida, uma lista vazia será usada.
        """
        super().__init__(nome, cpf)
        self.bagagens = bagagens if bagagens is not None else []

    def adicionar_bagagem(self, descricao: str, peso: float, session):
        """Adiciona uma nova bagagem ao passageiro e salva no banco de dados.

        Args:
            descricao (str): Descrição da bagagem.
            peso (float): Peso da bagagem em quilogramas.
            session: Sessão ativa do banco de dados para commit da bagagem.
        """
        nova_bagagem = Bagagem(descricao=descricao, peso=peso, passageiro_id=self.id)
        session.add(nova_bagagem)
        session.commit()
        self.bagagens.append(nova_bagagem)

    def listar_bagagens(self):
        """Lista todas as bagagens do passageiro, exibindo suas descrições e pesos."""
        if not self.bagagens:
            print("Nenhuma bagagem registrada.")
        else:
            for bagagem in self.bagagens:
                print(bagagem)

    def __repr__(self):
        """Retorna uma representação textual do passageiro para depuração.

        Returns:
            str: Representação formatada do passageiro.
        """
        return f"<Passageiro nome={self.nome} cpf={self.cpf} bagagens={len(self.bagagens)}>"