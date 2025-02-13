<<<<<<< Updated upstream
from sqlalchemy import Column, ForeignKey, Integer, String
=======
from sqlalchemy import Column, Float, ForeignKey, Integer, String
>>>>>>> Stashed changes
from sqlalchemy.orm import relationship
from services.base import Base

class Sacola(Base):
    __tablename__ = 'sacolas'

    id = Column(Integer, primary_key=True, autoincrement=True)
    vendedor_usuario = Column(String(255), ForeignKey('vendedores.usuario'), nullable=False)  # Altere para String
    cliente_cpf = Column(String(11), ForeignKey('clientes.cpf'), nullable=False)
    produtos = relationship('SacolaProduto', back_populates='sacola')

    def __init__(self, vendedor_id, cliente_id, produtos=None):
        self.vendedor_id = vendedor_id
        self.cliente_id = cliente_id
        self.produtos = produtos or []

    def __repr__(self):
        return f"<Sacola(id={self.id}, vendedor_id={self.vendedor_id}, cliente_id={self.cliente_id})>"

# Tabela intermediária para o relacionamento muitos-para-muitos entre Sacola e Produto
class SacolaProduto(Base):
    __tablename__ = 'sacola_produto'

    sacola_id = Column(Integer, ForeignKey('sacolas.id'), primary_key=True)
    produto_id = Column(String(13), ForeignKey('produtos_servicos.codigo'), primary_key=True)
<<<<<<< Updated upstream
=======
    lin_venda = Column(Integer, primary_key=True)
    quantidade = Column(Integer, nullable=False)
    valor_unit = Column(Float, nullable=False)
    total = Column(Float, nullable=False)
>>>>>>> Stashed changes

    # Relacionando a Sacola e ProdutoServico
    sacola = relationship('Sacola', back_populates='produtos')
    produto = relationship('ProdutoServico', back_populates='sacolas')

