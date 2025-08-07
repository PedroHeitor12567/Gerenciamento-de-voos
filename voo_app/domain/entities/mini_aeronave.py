class MiniAeronave:
    """Classe que representa uma aeronave simplificada, com modelo e capacidade.

    Attributes:
        modelo (str): Modelo da aeronave.
        capacidade (int): Quantidade máxima de passageiros suportada pela aeronave.
    """

    def __init__(self, modelo: str, capacidade: int):
        """Inicializa uma instância de MiniAeronave.

        Args:
            modelo (str): Modelo da aeronave.
            capacidade (int): Capacidade de passageiros da aeronave.
        """
        self.modelo = modelo
        self.capacidade = capacidade

    def resumo_voo(self) -> dict:
        """Retorna um resumo dos dados da aeronave.

        Returns:
            dict: Dicionário contendo o modelo e a capacidade da aeronave.
        """
        return {
            "Modelo": self.modelo,
            "Capacidade": self.capacidade
        }