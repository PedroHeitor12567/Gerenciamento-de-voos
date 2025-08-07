from voo_app.domain.entities.passageiro import Passageiro
from voo_app.domain.entities.funcionario import Funcionario
from voo_app.domain.entities.pessoa import Pessoa
from voo_app.domain.entities.mini_aeronave import MiniAeronave
from voo_app.interface_adapters.presenters.relatorio_builder import _RelatorioBuilder
from voo_app.infrastructure.database.models_method import listar_passageiros, listar_funcionarios, Session
from sqlalchemy.exc import NoResultFound

class Voo:
    """Classe que representa um voo com passageiros e tripulação.

    Attributes:
        numero_voo (str): Número identificador do voo.
        origem (str): Local de origem do voo.
        destino (str): Local de destino do voo.
        aeronave (MiniAeronave): Aeronave designada para o voo.
        passageiros (list[Passageiro]): Lista de passageiros cadastrados no voo.
        tripulacao (list[Funcionario]): Lista de funcionários (tripulação) do voo.
    """

    def __init__(self, numero_voo, origem, destino, aeronave: MiniAeronave):
        """Inicializa um voo com origem, destino e aeronave.

        Args:
            numero_voo (str): Número identificador do voo.
            origem (str): Local de partida do voo.
            destino (str): Local de chegada do voo.
            aeronave (MiniAeronave): Objeto representando a aeronave usada no voo.
        """
        self.numero_voo = numero_voo
        self.origem = origem
        self.destino = destino
        self.aeronave = aeronave
        self.passageiros: list[Passageiro] = []
        self.tripulacao: list[Funcionario] = []

    @staticmethod
    def adicionar_passageiro(db: Session, pessoa_id: int, voo_id: int, bagagem: str) -> Passageiro:
        """Adiciona um passageiro ao voo no banco de dados, com verificação de capacidade.

        Args:
            db (Session): Sessão ativa do banco de dados.
            pessoa_id (int): ID da pessoa a ser adicionada como passageiro.
            voo_id (int): ID do voo ao qual será associada.
            bagagem (str): Descrição da bagagem do passageiro.

        Returns:
            Passageiro: Objeto Passageiro recém-criado.

        Raises:
            ValueError: Se a pessoa ou voo não existirem, ou se o voo estiver lotado.
        """
        pessoa = db.query(Pessoa).filter(Pessoa.id == pessoa_id).first()
        if not pessoa:
            raise ValueError(f"Pessoa com ID {pessoa_id} não existe.")
        
        voo = db.query(Voo).filter(Voo.id == voo_id).first()
        if not voo:
            raise ValueError(f"Voo com ID {voo_id} não existe.")
        
        ja_eh_passageiro = db.query(Passageiro).filter(
            Passageiro.pessoa_id == pessoa_id,
            Passageiro.voo_id == voo_id
        ).first()

        if ja_eh_passageiro:
            raise ValueError(f"Pessoa ID {pessoa_id} já é passageira do voo ID {voo_id}.")
        
        total_passageiros = db.query(Passageiro).filter(
            Passageiro.voo_id == voo_id
        ).count()

        if total_passageiros >= voo.capacidade:
            raise ValueError(f"Voo ID {voo_id} está lotado. Capacidade máxima: {voo.capacidade} passageiros.")
        
        novo_passageiro = Passageiro(
            pessoa_id=pessoa_id,
            voo_id=voo_id,
            bagagem=bagagem
        )

        db.add(novo_passageiro)
        db.commit()
        db.refresh(novo_passageiro)
        return novo_passageiro

    def adicionar_tripulante(self, session, pessoa_id: int, cargo: str):
        """Adiciona um tripulante (funcionário) ao voo.

        Args:
            session: Sessão ativa do banco de dados.
            pessoa_id (int): ID da pessoa a ser promovida a funcionário.
            cargo (str): Cargo a ser atribuído ao funcionário.
        """
        try:
            pessoa = session.query(Pessoa).filter_by(id=pessoa_id).one()
        except NoResultFound:
            print("❌ Pessoa não encontrada.")
            return
        
        funcionario_existente = session.query(Funcionario).filter_by(pessoa_id=pessoa_id).first()
        if funcionario_existente:
            print("⚠️ Essa pessoa já é um funcionário.")
            return

        funcionario = Funcionario(pessoa_id=pessoa_id, cargo=cargo)
        session.add(funcionario)
        session.commit()
        print(f"✅ Funcionário {pessoa.nome} criado com sucesso com cargo: {cargo}.")

        if funcionario in self.tripulacao:
            print(f"⚠️ Funcionário {pessoa.nome} já está na tripulação do voo {self.numero_voo}.")
        else:
            self.tripulacao.append(funcionario)
            print(f"✈️ Funcionário {pessoa.nome} adicionado à tripulação do voo {self.numero_voo}.")

    def listar_passageiros(self):
        """Gera um relatório formatado de todos os passageiros do voo.

        Returns:
            str: Relatório formatado com colunas (ID, Nome, CPF, Bagagens).
        """
        construindo = _RelatorioBuilder("Todos os Passageiros")
        construindo.adicionar_colunas(
            ("ID", "cyan", "center"),
            ("Nome", "yellow", "center"),
            ("CPF", "green", "center"),
            ("Bagagens", "white", "center")
        )

        rows = listar_passageiros()
        for row in rows:
            construindo.adicionar_linhas(
                row[0],
                row[1],
                row[2],
                row[3]
            )
        
        return construindo.construir()
    
    def listar_tripulacao(self):
        """Gera um relatório formatado de todos os membros da tripulação do voo.

        Returns:
            str: Relatório formatado com colunas (ID, Nome, CPF, Bagagens).
        """
        construindo = _RelatorioBuilder("Todos os Funcionários")
        construindo.adicionar_colunas(
            ("ID", "cyan", "center"),
            ("Nome", "yellow", "center"),
            ("CPF", "green", "center"),
            ("Bagagens", "white", "center")
        )

        rows = listar_funcionarios()
        for row in rows:
            construindo.adicionar_linhas(
                row[0],
                row[1],
                row[2],
                row[3]
            )
        
        return construindo.construir()