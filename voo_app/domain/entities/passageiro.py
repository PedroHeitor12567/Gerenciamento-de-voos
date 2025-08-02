from domain.entities.pessoa import Pessoa

class Passageiro(Pessoa):
    def __init__(self, nome:str, cpf:str, bagagens:None):
        super().__init__(nome, cpf)
        self.bagagens = bagagens if bagagens is not None else []

    def adicionar_bagagens(self, descricao:str):
        self.bagagens.append(descricao)
    
    def listar_bagagens(self):
        for bagagem in self.bagagens:
            print(bagagem)
    
    def __repr__(self):
        return f"<Passageiro nome={self.nome} cpf={self.cpf} bagagens={len(self.bagagens)}>"