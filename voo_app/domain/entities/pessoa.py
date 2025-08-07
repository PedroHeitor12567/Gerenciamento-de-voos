class Pessoa:
    def __init__(self, nome:str, cpf:str):
        self._nome = nome
        self._cpf = cpf

    @property
    def nome(self):
        return self._nome

    @property
    def cpf(self):
        return self._cpf

    def __str__(self):
        return f"{self.nome} ({self.cpf})"

    def __str__(self):
        return f"Pessoa: {self.nome}"
