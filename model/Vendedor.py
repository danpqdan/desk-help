import bcrypt
from sqlalchemy import Column, String
from services.base import Base

class Vendedor(Base):
    __tablename__ = 'vendedores'
    
    usuario = Column(String(50), primary_key=True, nullable=False, unique=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    senha = Column(String(255), nullable=False)

    def __init__(self, usuario, nome, email, senha):
        self.usuario = usuario
        self.nome = nome
        self.email = email
        self.senha = self.hash_senha(senha)
    
    @staticmethod
    def hash_senha(senha: str) -> str:
        """Gera um hash seguro para a senha"""
        salt = bcrypt.gensalt()
        hashed_senha = bcrypt.hashpw(senha.encode(), salt)
        return hashed_senha.decode()
    
    def verificar_senha(senha: str, senha_hash: str) -> bool:
        """Verifica se a senha fornecida corresponde ao hash armazenado"""
        return bcrypt.checkpw(senha.encode(), senha_hash.encode())


    def __repr__(self):
        return f"<Vendedor(usuario={self.usuario}, nome={self.nome}, email={self.email})>"
