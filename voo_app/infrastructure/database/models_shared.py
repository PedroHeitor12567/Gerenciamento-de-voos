from sqlalchemy import Table, Column, Integer, ForeignKey
from infrastructure.database.models import Base

voo_passageiros = Table(
    "voo_passageiros", Base.metadata,
    Column("voo_id", Integer, ForeignKey("voos.id")),
    Column("passageiro_id", Integer, ForeignKey("passageiros.id"))
)

voo_tripulantes = Table(
    "voo_tripulantes", Base.metadata,
    Column("voo_id", Integer, ForeignKey("voos.id")),
    Column("funcionario_id", Integer, ForeignKey("funcionarios.id"))
)