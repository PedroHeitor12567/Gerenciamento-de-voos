from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from voo_app.infrastructure.database.models_shared import voo_passageiros, voo_tripulantes
from voo_app.infrastructure.database.connect import Base

class PessoaModel(Base):
    __tablename__ = "pessoas"

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    cpf = Column(String, unique=True, nullable=False)

    def __repr__(self):
        return f"<PessoaModel(nome='{self.nome}', cpf='{self.cpf}')>"
    
class PassageiroModel(Base):
    __tablename__ = "passageiros"

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    cpf = Column(String, unique=True, nullable=False)
    bagagens = Column(String, default="")

    def __repr__(self):
        return f"<PassageiroModel(nome='{self.nome}', cpf='{self.cpf}')>"   

class FuncionarioModel(Base):
    __tablename__ = "funcionarios"

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    cpf = Column(String, unique=True, nullable=False)
    matricula = Column(String, unique=True, nullable=False)
    cargo = Column(String, nullable=False)

    def __repr__(self):
        return f"<FuncionarioModel(nome='{self.nome}', cargo='{self.cargo}')>"

class MiniAeronaveModel(Base):
    __tablename__ = "aeronaves"

    id = Column(Integer, primary_key=True)
    modelo = Column(String, nullable=False)
    capacidade = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<AeronaveModel(modelo='{self.modelo}', capacidade={self.capacidade})>"
    
class VooModel(Base):
    __tablename__ = "voos"

    id = Column(Integer, primary_key=True)
    aeronave_id = Column(Integer, ForeignKey("aeronaves.id"))
    numero_voo = Column(String, unique=True, nullable=False)
    origem = Column(String, nullable=False)
    destino = Column(String, nullable=False)

    aeronave = relationship("MiniAeronaveModel")

    passageiros = relationship("PassageiroModel", secondary=voo_passageiros, backref="voos")
    tripulacao = relationship("FuncionarioModel", secondary=voo_tripulantes, backref="voos")

    def __repr__(self):
        return f"<VooModel(numero='{self.numero_voo}', origem='{self.origem}', destino='{self.destino}')>"

    def total_ocupantes(self):
        return len(self.passageiros) + len(self.tripulacao)

    def capacidade_excedida(self):
        if self.aeronave:
            return self.total_ocupantes() > self.aeronave.capacidade
        return False