from infrastructure.database.models import VooModel
from domain.entities.voo import Voo

def voo_from_db(voo_model: VooModel) -> Voo:
    return Voo(
        id=voo_model.id,
        numero=voo_model.numero,
        aeronave =voo_model.aeronave_id,
        origem=voo_model.origem,
        destino=voo_model.destino
    )