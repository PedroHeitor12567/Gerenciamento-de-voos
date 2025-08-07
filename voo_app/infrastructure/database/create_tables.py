from voo_app.infrastructure.database.connect import Base, engine
Base.metadata.create_all(bind=engine)