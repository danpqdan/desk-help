import re
import enum
from sqlalchemy import Column, String, Float, Enum
from sqlalchemy.orm import relationship
from services.base import Base

class TipoProdutoServico(enum.Enum):
    PRODUTO = "PRODUTO"
    SERVIÇO = "SERVIÇO"

    @staticmethod
    def validar_tipo(tipo: str) -> 'TipoProdutoServico':
        tipo_normalizado = tipo.upper()
        if tipo_normalizado not in [e.value for e in TipoProdutoServico]:
            raise ValueError(f"Tipo inválido! Deve ser 'TipoProdutoServico.PRODUTO' ou 'TipoProdutoServico.SERVIÇO'.")
        
        return TipoProdutoServico(tipo_normalizado)

class ProdutoServico(Base):
    __tablename__ = 'produtos_servicos'

    codigo = Column(String(13), primary_key=True, nullable=False, unique=True)
    descricao = Column(String(255), nullable=False)
    tipo = Column(Enum(TipoProdutoServico), nullable=False)
    valor = Column(Float, nullable=False)
    
    # Relacionamento reverso
    sacolas = relationship('SacolaProduto', back_populates='produto')
    
    def __init__(self, codigo, descricao, tipo, valor):
        self.codigo = self.validar_codigo_barras(codigo, tipo)
        self.descricao = descricao
        self.tipo = TipoProdutoServico.validar_tipo(tipo)
        self.valor = self.converter_valor(valor)
        
    def __repr__(self):
        return f"<ProdutoSacola(Codigo={self.codigo}, descrição={self.descricao}, tipo={self.tipo}, valor={self.valor})>"


    @staticmethod
    def validar_codigo_barras(codigo: str, tipo: TipoProdutoServico) -> str:
        if tipo == TipoProdutoServico.PRODUTO:
            if not re.fullmatch(r"\d{12,13}", codigo):
                raise ValueError("Código de barras inválido para produto! Deve conter 12 ou 13 dígitos numéricos.")
        return codigo

    @staticmethod
    def converter_valor(valor: int) -> float:
        try:
            valor_float = float(valor)
            return round(valor_float, 2)
        except ValueError:
            raise ValueError(f"Valor inválido: {valor}")