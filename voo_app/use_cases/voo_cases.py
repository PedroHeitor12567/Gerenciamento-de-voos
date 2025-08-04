from infrastructure.database.models import PassageiroModel, FuncionarioModel, MiniAeronaveModel, VooModel
from sqlalchemy.orm import Session

class VooCases:
    def __init__(self, db: Session):
        self.db = db
    
    def criar_voo(self, voo_id: int, aeronave_id: int, numero_voo: str, origem: str, destino: str):
        aeronave = self.db.query(MiniAeronaveModel).filter_by(id=aeronave_id).first()
        if not aeronave:
            raise ValueError("Aeronave não cadastrada no banco de dados!")
        
        create_voo = VooModel(
            aeronave_id = aeronave_id,
            numero_voo = numero_voo,
            origem = origem,
            destino = destino
        )

        self.db.add(create_voo)
        self.db.commit()
        self.db.refresh(create_voo)

        return create_voo
    
    def listar_voos(self, numero_voo: str):
        voos = self.db.query(VooModel).filter_by(numero_voo).all()
        l_voos = list
        for voo in voos:
            l_voos.append(voo)
        return l_voos

    def deletar_voo(self, numero_voo: str):
        voo = self.db.query(VooModel).filter_by(numero_voo=numero_voo).first()
        if not voo:
            raise ValueError("Voo não cadastrado no banco de dados!")
        
        self.db.delete(voo)
        self.db.commit()

        return voo

    def buscar_voo(self, numero_voo: str):
        voo = self.db.query(VooModel).filter_by(numero_voo).first()
        if voo:
            raise ValueError("Voo não encontrado!")
        
