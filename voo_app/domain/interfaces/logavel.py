from abc import ABC, abstractmethod

class Logavel(ABC):
    @abstractmethod
    def logar_entrada(self):
        return f"Usuário {self.nome} fez login!"