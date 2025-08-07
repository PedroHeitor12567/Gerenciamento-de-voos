from voo_app.interface_adapters.presenters.relatorio_builder import _RelatorioBuilder
from voo_app.infrastructure.database.models_method import listar_voos
from voo_app.infrastructure.database.models import VooModel
from voo_app.infrastructure.database.connect import SessionLocal
from voo_app.domain.mixins.identificavel import gerar_id
from .mini_aeronave import MiniAeronave

class CompanhiaAerea:
    """Classe que representa uma companhia aérea, responsável por gerenciar seus voos.

    Attributes:
        nome (str): Nome da companhia aérea.
        voos (list): Lista de voos associados à companhia.
    """

    def __init__(self, nome: str):
        """Inicializa a companhia aérea com um nome e uma lista de voos.

        Args:
            nome (str): Nome da companhia aérea. Deve ter pelo menos 3 caracteres.
        """
        if len(nome) < 3:
            print("Nome inválido. Deve ter pelo menos 3 caracteres.")
            self.nome = "Nome inválido"
        else:
            self.nome = nome
        self.voos = []

    @property
    def nome(self):
        """Getter para o nome da companhia aérea.

        Returns:
            str: Nome da companhia.
        """
        return self._nome

    @nome.setter
    def nome(self, novo_nome: str):
        """Setter para o nome da companhia aérea. Valida o tamanho do nome.

        Args:
            novo_nome (str): Novo nome a ser atribuído à companhia.
        """
        if len(novo_nome) < 3:
            print("Nome inválido. Deve ter pelo menos 3 caracteres.")
        else:
            self._nome = novo_nome
            print(f"Nome atualizado para: {self._nome}.")

    @staticmethod
    def cadastrar_voo(origem: str, destino: str, aeronave_id: int):
        """Cadastra um novo voo diretamente no banco de dados (modo estático).

        Args:
            origem (str): Cidade de origem do voo.
            destino (str): Cidade de destino do voo.
            aeronave_id (int): ID da aeronave usada no voo.

        Returns:
            VooModel or None: Objeto do voo cadastrado ou None em caso de erro.
        """
        db = SessionLocal()
        numero_voo = gerar_id()

        try:
            voo_existente = db.query(VooModel).filter_by(numero_voo=numero_voo).first()
            if voo_existente:
                print(f"❌ Voo com número {numero_voo} já está cadastrado.")
                return None

            novo_voo = VooModel(
                numero_voo=numero_voo,
                origem=origem,
                destino=destino,
                aeronave_id=aeronave_id
            )

            db.add(novo_voo)
            db.commit()
            db.refresh(novo_voo)

            print(f"✅ Voo {numero_voo} cadastrado com sucesso")
            return novo_voo

        except Exception as e:
            db.rollback()
            print("❌ Erro ao cadastrar voo:", e)
            return None
        finally:
            db.close()

    def cadastrar_voo_banco(self, origem: str, destino: str, aeronave: MiniAeronave):
        """Cadastra um novo voo e associa à companhia aérea atual.

        Args:
            origem (str): Cidade de origem.
            destino (str): Cidade de destino.
            aeronave (MiniAeronave): Objeto da aeronave utilizada no voo.

        Returns:
            VooModel or None: Objeto do voo criado, ou None se houver erro.
        """
        db = SessionLocal()
        numero_voo = gerar_id()
        try:
            voo_existente = db.query(VooModel).filter_by(numero_voo=numero_voo).first()
            if voo_existente:
                print(f"❌ Voo com número {numero_voo} já está cadastrado.")
                return None

            novo_voo = VooModel(
                numero_voo=numero_voo,
                origem=origem,
                destino=destino,
                aeronave_id=aeronave.id,
                companhia_nome=self.nome
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
        """Busca um voo pelo número no banco de dados.

        Args:
            numero (str): Número identificador do voo.

        Returns:
            VooModel or None: Objeto do voo encontrado ou None.
        """
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
        """Lista todos os voos disponíveis no sistema com um relatório formatado.

        Returns:
            str: Relatório com todos os voos formatado usando o builder.
        """
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
        """Adiciona um voo manualmente à base de dados (sem checagem de duplicidade).

        Args:
            numero_voo (str): Número identificador do voo.
            origem (str): Cidade de origem.
            destino (str): Cidade de destino.
            aeronave (MiniAeronave): Aeronave que será usada no voo.
        """
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