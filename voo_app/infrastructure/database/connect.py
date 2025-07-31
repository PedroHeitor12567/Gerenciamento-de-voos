from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from sqlalchemy import text
from dotenv import load_dotenv
import os

load_dotenv()

DB_URL = os.getenv("DB_URL")
engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def testar_conexao():
    try:
        with engine.connect() as conexao:
            conexao.execute(text("SELECT 1"))  # comando simples
        print("✅ Conexão com o banco estabelecida com sucesso!")
    except OperationalError as e:
        print("❌ Erro ao conectar no banco de dados:")
        print(e)

if __name__ == "__main__":
    testar_conexao()