from .connect import engine, SessionLocal
from .models import PessoaModel, FuncionarioModel, PassageiroModel, MiniAeronaveModel, VooModel, CompanhiasModel
from sqlalchemy import text
from sqlalchemy.orm import Session

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
def mudar_nome_companhia(novo_nome: str):
    db = SessionLocal()
    companhia = db.query(CompanhiasModel).filter_by(nome=novo_nome).first()
    if not companhia:
        print("❌ Companhia não encontrada!")
        db.close()
        return

    try:
        # Aqui você pode atualizar outros campos se necessário
        print(f"✅ Companhia encontrada: {novo_nome}")
    except Exception as e:
        db.rollback()
        print("❌ Erro ao buscar companhia:", e)
    finally:
        db.close()

def listar_companhias():
    with engine.connect() as conn:
        resultado = conn.execute(text("SELECT * FROM companhias"))
        rows = resultado.fetchall()
    return rows