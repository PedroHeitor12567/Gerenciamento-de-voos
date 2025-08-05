class CompanhiaAerea:
    def __init__(self, nome: str):
        if len(nome) < 3:
            print("Nome inválido. Deve ter pelo menos 3 caracteres.")
            self.nome = "Nome inválido"
        else:
            self.nome = nome
        self.voos =[]


    @property
    def nome(self):
      return self._nome
    
    @nome.setter
    def nome(self, novo_nome: str):
        if len(novo_nome) < 3:
            print("Nome inválido. Deve ter pelo menos 3 caracteres.")
        else:
            self.nome = novo_nome
            print(f"Nome atualizado para: {self.nome}.")

    def adicionar_voo(self, voo):
        self.voos_append(voo)
        print(f"Voo {voo.numero_voo} adicionado na companhia.")

    def buscar_voo(self, numero: str):
        for voo in self.voos:
            if voo.numero_voo == numero:
                return voo
        print(f"Voo {numero} não foi encontrado.")

    def listar_voos(self):
        print(f"Voos da companhia {self.nome}: ")
        if not self.voos:
            print("Nenhum voo foi encontrado.")
        for voo in self.voos:
            print(f"- Voo {voo.numero_voo}: {voo.origem} para {voo.destino}.")