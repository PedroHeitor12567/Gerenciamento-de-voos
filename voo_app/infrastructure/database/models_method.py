from .connect import engine, SessionLocal
from .models import PessoaModel, FuncionarioModel, PassageiroModel, MiniAeronaveModel, VooModel, CompanhiasModel
from voo_app.domain.entities.mini_aeronave import MiniAeronave
from sqlalchemy import text
from rich.console import Console
from sqlalchemy.orm import Session
from voo_app.interface_adapters.presenters.relatorio_builder import _RelatorioBuilder
from voo_app.domain.mixins.identificavel import gerar_id  # ajuste o caminho se necessário

def listar_pessoas():
    with engine.connect() as conn:
        resultado = conn.execute(text("SELECT * FROM pessoas"))
        rows = resultado.fetchall()
    return rows

def listar_passageiros():
    with engine.connect() as conn:
        resultado = conn.execute(text("SELECT * FROM passageiros"))
        rows = resultado.fetchall()
    return rows

def listar_funcionarios():
    with engine.connect() as conn:
        resultado = conn.execute(text("SELECT * FROM funcionarios"))
        rows = resultado.fetchall()
    return rows

def listar_aeronaves():
    with engine.connect() as conn:
        resultado = conn.execute(text("SELECT * FROM aeronaves"))
        rows = resultado.fetchall()
    return rows

def listar_voos():
    with engine.connect() as conn:
        resultado = conn.execute(text("SELECT * FROM voos"))
        rows = resultado.fetchall()
    return rows

def cadastrar_pessoa(nome: str, cpf: str):
    db = SessionLocal()
    nova_pessoa = PessoaModel(nome=nome, cpf=cpf)

    try:
        db.add(nova_pessoa)
        db.commit()
        db.refresh(nova_pessoa)
        print("✅ Pessoa cadastrada com sucesso!")
    except Exception as e:
        db.rollback()
        print("❌ Erro ao cadastrar pessoa:", e)
    
    finally:
        db.close()

def cadastrar_companhia(nome: str):
    db = SessionLocal()
    nova_companhia = CompanhiasModel(nome=nome)
    companhia_existente = db.query(CompanhiasModel).filter_by(nome=nome).first()
    if companhia_existente:
        print("❌ Companhia já cadastrada!")
        db.close()
        return
    try:
        db.add(nova_companhia)
        db.commit()
        db.refresh(nova_companhia)
        print("✅ Companhia cadastrada com sucesso!")
    except Exception as e:
        db.rollback()
        print("❌ Erro ao cadastrar companhia:", e)
    
    finally:
        db.close()
def mudar_nome_companhia(nome_atual: str, novo_nome: str):
    db = SessionLocal()
    companhia = db.query(CompanhiasModel).filter_by(nome=nome_atual).first()
    if not companhia:
        print("❌ Companhia não encontrada!")
        db.close()
        return

    try:
        companhia.nome = novo_nome
        db.commit()
        print(f"✅ Nome da companhia alterado para: {novo_nome}")
    except Exception as e:
        db.rollback()
        print("❌ Erro ao alterar nome da companhia:", e)
    finally:
        db.close()

def listar_companhias():
    with engine.connect() as conn:
        resultado = conn.execute(text("SELECT * FROM companhias"))
        rows = resultado.fetchall()
    return rows

def tabela_pessoas():
    construtor = _RelatorioBuilder("Lista de Pessoas")
    construtor.adicionar_colunas(
        ("ID", "cyan", "center"),
        ("Nome", "yellow", "center"),
        ("CPF", "green", "center")
    )

    rows = listar_pessoas()
    for row in rows:
        construtor.adicionar_linhas(
            row[0],
            row[1],
            row[2]
        )
    tabela = construtor.construir()
    console = Console()
    console.print(tabela)

def tabela_companhias():
    construtor = _RelatorioBuilder("Lista de Companhias")
    construtor.adicionar_colunas(
        ("ID", "cyan", "center"),
        ("Nome", "yellow", "center")
    )

    rows = listar_companhias()
    for row in rows:
        construtor.adicionar_linhas(
            row[0],
            row[1]
        )
    tabela = construtor.construir()
    console = Console()
    console.print(tabela)

def tabela_passageiros():
    construtor = _RelatorioBuilder("Lista de Passageiros")
    construtor.adicionar_colunas(
        ("ID", "cyan", "center"),
        ("Nome", "yellow", "center"),
        ("CPF", "green", "center"),
        ("Bagagens", "white", "center")
    )

    rows = listar_passageiros()
    for row in rows:
        construtor.adicionar_linhas(
            row[0],
            row[1],
            row[2],
            row[3]
        )
    tabela = construtor.construir()
    console = Console()
    console.print(tabela)

def add_miniaeronave_db(aeronave: MiniAeronave):
    db = SessionLocal()
    try:
        # Cria uma instância de MiniAeronaveModel a partir do objeto MiniAeronave
        nova_aeronave = MiniAeronaveModel(
            modelo=aeronave.modelo,
            capacidade=aeronave.capacidade,
        )
        db.add(nova_aeronave)
        db.commit()
        db.refresh(nova_aeronave)
        print("✅ Aeronave cadastrada com sucesso!")
    except Exception as e:
        db.rollback()
        print("❌ Erro ao cadastrar aeronave:", e)
    finally:
        db.close()

def tabela_funcionarios():
    construtor = _RelatorioBuilder("Lista de Funcionários")
    construtor.adicionar_colunas(
        ("ID", "cyan", "center"),
        ("Nome", "yellow", "center"),
        ("CPF", "green", "center"),
        ("Matrícula", "light_green", "center"),
        ("Cargo", "white", "center")
    )

    rows = listar_funcionarios()
    for row in rows:
        construtor.adicionar_linhas(
            row[0],
            row[1],
            row[2],
            row[3],
            row[4]
        )
    tabela = construtor.construir()
    console = Console()
    console.print(tabela)

def tabela_voo():
    construtor = _RelatorioBuilder("Lista de Voos")
    construtor.adicionar_colunas(
        ("ID", "cyan", "center"),
        ("Aeronave", "white", "center"),
        ("Número", "cyan", "center"),
        ("Origem", "yellow", "center"),
        ("Destino", "green", "center"),
    )

    rows = listar_voos()
    for row in rows:
        construtor.adicionar_linhas(
            row[0],
            row[1],
            row[2],
            row[3],
            row[4]
        )
    tabela = construtor.construir()
    console = Console()
    console.print(tabela)

def cadastrar_passageiro(nome: str, cpf: str, bagagens=None):
    db = SessionLocal()
    novo_passageiro = PassageiroModel(nome=nome, cpf=cpf, bagagens=bagagens)

    try:
        db.add(novo_passageiro)
        db.commit()
        db.refresh(novo_passageiro)
        print("✅ Passageiro cadastrado com sucesso!")
    except Exception as e:
        db.rollback()
        print("❌ Erro ao cadastrar passageiro:", e)
    
    finally:
        db.close()
    

def cadastrar_voo(origem: str, destino: str, aeronave_id: int):
    db = SessionLocal()

    try:
        # Gera um número de voo único
        while True:
            numero_voo = gerar_id()
            voo_existente = db.query(VooModel).filter_by(numero_voo=numero_voo).first()
            if not voo_existente:
                break  # número de voo é único, pode usar

        # Cria o objeto do novo voo
        novo_voo = VooModel(
            aeronave_id=aeronave_id,
            numero_voo=numero_voo,
            origem=origem,
            destino=destino
        )

        db.add(novo_voo)
        db.commit()
        db.refresh(novo_voo)

        print(f"✅ Voo {numero_voo} cadastrado com sucesso.")
        return novo_voo

    except Exception as e:
        db.rollback()
        print("❌ Erro ao cadastrar voo:", e)

    finally:
        db.close()

def tabela_aeronaves():
    construtor = _RelatorioBuilder("Lista de Aeronaves")
    construtor.adicionar_colunas(
        ("ID", "cyan", "center"),
        ("Modelo", "yellow", "center"),
        ("Capacidade", "green", "center")
    )

    rows = listar_aeronaves()
    for row in rows:
        construtor.adicionar_linhas(
            row[0],
            row[1],
            row[2]
        )
    tabela = construtor.construir()
    console = Console()
    console.print(tabela)

def cadastrar_funcionario(nome: str, cpf: str, cargo: str):
    db = SessionLocal()
    try:
        # Busca a pessoa já cadastrada pelo nome e cpf
        pessoa = db.query(PessoaModel).filter_by(nome=nome, cpf=cpf).first()
        if not pessoa:
            print("❌ Pessoa não encontrada! Cadastre a pessoa antes de torná-la funcionário.")
            return

        matricula = str(gerar_id())
        novo_funcionario = FuncionarioModel(
            nome=pessoa.nome,
            cpf=pessoa.cpf,
            matricula=matricula,
            cargo=cargo
        )
        db.add(novo_funcionario)
        db.commit()
        db.refresh(novo_funcionario)
        print("✅ Funcionário cadastrado com sucesso!")
    except Exception as e:
        db.rollback()
        print("❌ Erro ao cadastrar funcionário:", e)
    finally:
        db.close()