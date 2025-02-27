from datetime import UTC, datetime
import enum
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, func, Enum
from sqlalchemy.orm import relationship
from services.base import Base

class Status(enum.Enum):
    EM_ANDAMENTO = "EM_ANDAMENTO"
    FINALIZADA = "FINALIZADA"
    CANCELADA = "CANCELADA"

class Sacola(Base):
    __tablename__ = 'sacolas'

    id = Column(Integer, primary_key=True, autoincrement=True)
    vendedor_usuario = Column(String(255), ForeignKey('vendedores.usuario'), nullable=False)
    cliente_cpf = Column(String(11), ForeignKey('clientes.cpf'), nullable=False)
    time_stamp = Column(DateTime, default=lambda: datetime.now(UTC))
    status = Column(Enum(Status), nullable=False)
    produtos = relationship('SacolaProduto', back_populates='sacola', cascade='all, delete-orphan')

    def __init__(self, vendedor_id, cliente_id, produtos=None):
        self.vendedor_id = vendedor_id
        self.cliente_id = cliente_id
        self.status = Status.EM_ANDAMENTO
        self.produtos = produtos or []
    def __repr__(self):
        return f"<Sacola(id={self.id}, vendedor_id={self.vendedor_usuario}, cliente_id={self.cliente_cpf})>"

class SacolaProduto(Base):
    __tablename__ = 'sacola_produto'

    sacola_id = Column(Integer, ForeignKey('sacolas.id', ondelete="CASCADE"), primary_key=True)
    produto_id = Column(String(13), ForeignKey('produtos_servicos.codigo'), primary_key=True)
    lin_venda = Column(Integer, primary_key=True)
    quantidade = Column(Integer, nullable=False)
    valor_unit = Column(Float, nullable=False)
    total = Column(Float, nullable=False)

    def __init__(self, sacola_id: int, produto_id: str, quantidade: int, valor_unit: float, total: float, session=None):
        self.sacola_id = sacola_id
        self.produto_id = produto_id
        self.lin_venda = self.obter_proximo_lin_venda(session, sacola_id)
        self.quantidade = quantidade
        self.valor_unit = valor_unit
        self.total = total

    @staticmethod
    def obter_proximo_lin_venda(session, sacola_id):
        proximo_lin_venda = (
            session.query(func.coalesce(func.max(SacolaProduto.lin_venda), 0) + 1)
            .filter(SacolaProduto.sacola_id == sacola_id)
            .scalar()
        )
        return proximo_lin_venda

    # Relacionamento com a Sacola e ProdutoServico
    sacola = relationship('Sacola', back_populates='produtos')
    produto = relationship('ProdutoServico', back_populates='sacolas')
