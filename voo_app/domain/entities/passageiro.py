from domain.entities.pessoa import Pessoa
from domain.entities.bagagem import Bagagem

class Passageiro(Pessoa):
    def __init__(self, nome: str, cpf: str, bagagens: list[Bagagem] = None):
        super().__init__(nome, cpf)
        self.bagagens = bagagens if bagagens is not None else []

    def adicionar_bagagem(self, descricao: str, peso: float):
        nova_bagagem = Bagagem(descricao, peso)
        self.bagagens.append(nova_bagagem)

    def listar_bagagens(self):
        if not self.bagagens:
            print("Nenhuma bagagem registrada.")
        else:
            for bagagem in self.bagagens:
                print(bagagem)

    def __repr__(self):
        return f"<Passageiro nome={self.nome} cpf={self.cpf} bagagens={len(self.bagagens)}>"