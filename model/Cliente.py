import re
from sqlalchemy import Column, String
from services.base import Base
import bcrypt


class Cliente(Base):
    __tablename__ = 'clientes'

    # Definindo os campos da tabela
    cpf = Column(String(11), primary_key=True)
    nome = Column(String(100), nullable=False)
    telefone = Column(String(15), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    senha = Column(String(20), nullable=False)

    def __repr__(self):
        return f"Cliente(cpf={self.cpf}, nome={self.nome}, telefone={self.telefone}, email={self.email})"
    
    def __init__(self, cpf, nome, telefone, email, senha):
        self.cpf = self.limpar_cpf(cpf)
        self.nome = nome
        self.telefone = self.formatar_telefone(telefone)
        self.email = self.validar_email(email)
        self.senha = self.hash_senha(senha)
    
    def hash_senha(senha: str) -> str:
        """Gera um hash seguro para a senha"""
        salt = bcrypt.gensalt()
        hashed_senha = bcrypt.hashpw(senha.encode(), salt)
        return hashed_senha.decode()
    
    def verificar_senha(senha: str, senha_hash: str) -> bool:
        """Verifica se a senha fornecida corresponde ao hash armazenado"""
        return bcrypt.checkpw(senha.encode(), senha_hash.encode())

    def limpar_cpf(cpf: str) -> str:
        """Remove pontos e traços do CPF, mantendo apenas os números."""
        return re.sub(r'\D', '', cpf) 
    
    def validar_email(email: str) -> bool:
        """Verifica se o e-mail tem um formato válido."""
        padrao_email = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(padrao_email, email) is not None

    def formatar_telefone(telefone: str) -> str:
        """Remove pontuações e formata o número no padrão DDD + número."""
        telefone_limpo = re.sub(r'\D', '', telefone)  # Remove tudo que não for número
        if len(telefone_limpo) == 11:  # Confere se tem o tamanho correto
            return telefone_limpo
        raise ValueError("Número de telefone inválido! Deve conter 11 dígitos.")


