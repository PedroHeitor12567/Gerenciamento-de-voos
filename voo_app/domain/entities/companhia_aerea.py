from voo_app.interface_adapters.presenters.relatorio_builder import _RelatorioBuilder
from voo_app.infrastructure.database.models_method import listar_voos
from voo_app.infrastructure.database.models import VooModel
from voo_app.infrastructure.database.connect import engine, SessionLocal
from voo_app.domain.mixins.identificavel import gerar_id
from .mini_aeronave import MiniAeronave

class CompanhiaAerea:
    def __init__(self, nome: str):
        if len(nome) < 3:
            print("Nome inválido. Deve ter pelo menos 3 caracteres.")
            self.nome = "Nome inválido"
        else:
            self.nome = nome
        self.voos =[]


    @property
    def nome(self):
      return self._nome
    
    @nome.setter
    def nome(self, novo_nome: str):
        if len(novo_nome) < 3:
            print("Nome inválido. Deve ter pelo menos 3 caracteres.")
        else:
            self.nome = novo_nome
            print(f"Nome atualizado para: {self.nome}.")

    def cadastrar_voo(origem: str, destino: str, aeronave_id: int):
        db = SessionLocal()
        numero_voo = gerar_id()

        try:
            # Verifica se o voo já existe
            voo_existente = db.query(VooModel).filter_by(numero_voo=numero_voo).first()
            if voo_existente:
                print(f"❌ Voo com número {numero_voo} já está cadastrado.")
                return None

            # Gera ID aleatório para o voo

            # Cria o novo objeto de voo
            novo_voo = VooModel(
                numero_voo=numero_voo,
                origem=origem,
                destino=destino,
                aeronave_id=aeronave_id
            )

            db.add(novo_voo)
            db.commit()
            db.refresh(novo_voo)

            print(f"✅ Voo {numero_voo} cadastrado com sucesso (ID: {voo_id})")
            return novo_voo

        except Exception as e:
            db.rollback()
            print("❌ Erro ao cadastrar voo:", e)

        finally:
            db.close()

    def cadastrar_voo_banco(self, origem: str, destino: str, aeronave: MiniAeronave):
        db = SessionLocal()
        numero_voo = gerar_id()
        try:
            # Verifica se o voo já existe
            voo_existente = db.query(VooModel).filter_by(numero_voo=numero_voo).first()
            if voo_existente:
                print(f"❌ Voo com número {numero_voo} já está cadastrado.")
                return None

            # Cria o novo objeto de voo, associando à companhia aérea
            novo_voo = VooModel(
            numero_voo=numero_voo,
            origem=origem,
            destino=destino,
            aeronave_id=aeronave.id,
            companhia_nome=self.nome  # Supondo que exista esse campo no modelo
            )

            db.add(novo_voo)
            db.commit()
            db.refresh(novo_voo)
            print(f"✅ Voo {numero_voo} cadastrado com sucesso e associado à companhia {self.nome}!")
            self.voos.append(novo_voo)
            return novo_voo

        except Exception as e:
            db.rollback()
            print("❌ Erro ao cadastrar voo:", e)
            return None
        finally:
            db.close()


    def buscar_voo(self, numero: str):
        db = SessionLocal()
        try:
            voo = db.query(VooModel).filter_by(numero_voo=numero).first()
            if voo:
                return voo
            print(f"Voo {numero} não foi encontrado.")
            return None
        except Exception as e:
            print("❌ Erro ao buscar voo:", e)
            return None
        finally:
            db.close()

    def listar_voos(self):
        construindo = _RelatorioBuilder("Todos os Voos")
        construindo.adicionar_colunas(
            ("Número", "cyan", "center"),
            ("Origem", "yellow", "center"),
            ("Destino", "green", "center"),
            ("Aeronave", "white", "center")
        )

        rows = listar_voos()
        for row in rows:
            construindo.adicionar_linhas(
                row[0],
                row[1],
                row[2],
                row[3]
            )
        
        return construindo.construir()
    
    def adicionar_voo(self, numero_voo: str, origem: str, destino: str, aeronave: MiniAeronave):
        db = SessionLocal()
        novo_voo = VooModel(numero_voo=numero_voo, origem=origem, destino=destino, aeronave=aeronave)

        try:
            db.add(novo_voo)
            db.commit()
            db.refresh(novo_voo)
            print("✅ Voo cadastrado com sucesso!")
        except Exception as e:
            db.rollback()
            print("❌ Erro ao cadastrar voo:", e)

        finally:
            db.close()