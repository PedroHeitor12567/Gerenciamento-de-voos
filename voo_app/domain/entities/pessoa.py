class Pessoa:
    """Classe base que representa uma pessoa com nome e CPF.

    Attributes:
        _nome (str): Nome da pessoa (acessado via propriedade `nome`).
        _cpf (str): CPF da pessoa (acessado via propriedade `cpf`).
    """

    def __init__(self, nome: str, cpf: str):
        """Inicializa uma instância da classe Pessoa.

        Args:
            nome (str): Nome da pessoa.
            cpf (str): CPF da pessoa.
        """
        self._nome = nome
        self._cpf = cpf

    @property
    def nome(self) -> str:
        """Obtém o nome da pessoa.

        Returns:
            str: Nome da pessoa.
        """
        return self._nome

    @property
    def cpf(self) -> str:
        """Obtém o CPF da pessoa.

        Returns:
            str: CPF da pessoa.
        """
        return self._cpf

    def __str__(self) -> str:
        """Retorna uma representação textual simples da pessoa.

        Returns:
            str: String com nome e CPF da pessoa.
        """
        return f"Pessoa: {self.nome} ({self.cpf})"