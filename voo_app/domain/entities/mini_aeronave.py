class MiniAeronave:
    def __init__(self, modelo: str, capacidade: int):
        self.modelo = modelo
        self.capacidade = capacidade
    
    def resumo_voo(self) -> dict:
        return {
            "Modelo": self.modelo,
            "Capacidade": self.capacidade
        }