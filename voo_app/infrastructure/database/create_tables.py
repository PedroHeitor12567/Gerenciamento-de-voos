from connect import Base, engine
import models_shared
import models
Base.metadata.create_all(bind=engine)