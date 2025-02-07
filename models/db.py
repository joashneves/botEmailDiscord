from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine("sqlite:///dados.db")
Base = declarative_base()
_Sessao = sessionmaker(engine)

class ServidorBase(Base):
    __tablename__ = "servidorBase"
    id = Column(Integer, primary_key=True)
    id_servidor = Column(Integer, nullable=False)
    email = Column(String(50))

class Usuario(Base):
    __tablename__ = "usuario"
    id = Column(Integer, primary_key=True)
    id_discord = Column(Integer, nullable=False)
    aceita_dm = Column(Boolean, default=True )
    apelido = Column(String(25))
    descricao = Column(String(255))
    post = Column(Integer)
    id_ServidorBase = Column(Integer, ForeignKey("servidorBase.id"))

class Seguindo(Base):
    __tablename__ = "seguindo"
    id = Column(Integer, primary_key=True)
    id_usuario_seguidor = Column(Integer, ForeignKey("usuario.id"))
    id_usuario_alvo = Column(Integer, ForeignKey("usuario.id"))

class UsuariosBanidos(Base):
    __tablename__ = "usuariosBanidos"
    id = Column(Integer, primary_key=True)
    id_usuario_banido = Column(Integer, ForeignKey("usuario.id"))
    motivo = Column(String)

class FeedConfig(Base):
    __tablename__ = "feedConfig"
    id = Column(Integer, primary_key=True, index=True)
    id_ServidorBase = Column(Integer, ForeignKey("servidorBase.id"))
    id_chat = Column(Integer, nullable=False, index=True)

Base.metadata.create_all(engine)