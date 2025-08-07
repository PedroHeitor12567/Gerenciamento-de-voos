from voo_app.domain.entities.passageiro import Passageiro
from voo_app.domain.entities.funcionario import Funcionario
from voo_app.domain.entities.pessoa import Pessoa
from voo_app.domain.entities.mini_aeronave import MiniAeronave
from voo_app.interface_adapters.presenters.relatorio_builder import _RelatorioBuilder
from voo_app.infrastructure.database.models_method import listar_passageiros, listar_funcionarios, Session
from sqlalchemy.exc import NoResultFound
class Voo:
    def __init__(self, numero_voo, origem, destino, aeronave: MiniAeronave):
        self.numero_voo = numero_voo
        self.origem = origem
        self.destino = destino
        self.aeronave = aeronave
        self.passageiros: list[Passageiro] = []
        self.tripulacao: list[Funcionario] = []

    def adicionar_passageiro(db: Session, pessoa_id: int, voo_id: int, bagagem: str) -> Passageiro:
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
        