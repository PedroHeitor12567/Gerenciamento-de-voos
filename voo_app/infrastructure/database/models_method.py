from .connect import engine, SessionLocal
from .models import PessoaModel, FuncionarioModel, PassageiroModel, MiniAeronaveModel, VooModel
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