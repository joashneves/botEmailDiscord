from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine("sqlite:///dados.db")
Base = declarative_base()
_Sessao = sessionmaker(engine)

class ServidorBase(Base):
    __tablename__ = "ServidorBase"
    id = Column(Integer, primary_key=True)
    id_servidor = Column(Integer, nullable=False)
    email = Column(String)

class Usuario(Base):
    __tablename__ = "Usuario"
    id = Column(Integer, primary_key=True)
    id_discord = Column(Integer, nullable=False)
    apelido = Column(String)
    descricao = Column(String)
    post = Column(Integer)
    id_ServidorBase = Column(Integer, ForeignKey("ServidorBase.id"))

Base.metadata.create_all(engine)