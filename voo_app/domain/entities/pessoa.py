class Pessoa:
    def __init__(self, nome:str, cpf:str):
        self.nome = nome
        self.cpf = cpf
    
    def __str__(self):
        return f"Pessoa: {self.nome}"
