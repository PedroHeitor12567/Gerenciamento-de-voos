class Bagagem:
    """Classe que representa uma bagagem com descrição e peso.

    Attributes:
        descricao (str): Descrição do conteúdo da bagagem.
        peso (float): Peso da bagagem em quilogramas.
    """

    def __init__(self, descricao: str, peso: float):
        """Inicializa uma instância de Bagagem.

        Args:
            descricao (str): Descrição do conteúdo da bagagem.
            peso (float): Peso da bagagem em quilogramas.
        """
        self.descricao = descricao
        self.peso = peso

    def __str__(self):
        """Retorna uma representação textual da bagagem.

        Returns:
            str: Descrição e peso da bagagem formatados como string.
        """
        return f"{self.descricao} – {self.peso} kg"