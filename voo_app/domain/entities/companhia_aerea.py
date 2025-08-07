from interface_adapters.presenters.relatorio_builder import _RelatorioBuilder
from infrastructure.database.models_method import listar_voos
from infrastructure.database.models import VooModel
from infrastructure.database.connect import engine, SessionLocal
from mini_aeronave import MiniAeronave

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

    def adicionar_voo(self, voo):
        self.voos_append(voo)
        print(f"Voo {voo.numero_voo} adicionado na companhia.")

    def buscar_voo(self, numero: str):
        for voo in self.voos:
            if voo.numero_voo == numero:
                return voo
        print(f"Voo {numero} não foi encontrado.")

    def listar_voos():
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
