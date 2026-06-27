import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app.infrastructure.database import db

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='funcionario')
    ativo = db.Column(db.Boolean, default=True)
    criado_em = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def set_senha(self, senha):
        # gera hash da senha
        self.senha_hash = generate_password_hash(senha)

    def verificar_senha(self, senha):
        # valida se a senha digitada bate com a salva
        return check_password_hash(self.senha_hash, senha)

    def to_dict(self):
        # converte os dados do usuario para enviar como JSON
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'role': self.role,
            'ativo': self.ativo,
            'criado_em': self.criado_em.isoformat() if self.criado_em else None
        }

class Unidade(db.Model):
    __tablename__ = 'unidades'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    cidade = db.Column(db.String(100), nullable=False)
    ativo = db.Column(db.Boolean, default=True)

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'cidade': self.cidade,
            'ativo': self.ativo
        }

class Produto(db.Model):
    __tablename__ = 'produtos'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Numeric(10, 2), nullable=False)
    ativo = db.Column(db.Boolean, default=True)

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'preco': float(self.preco),
            'ativo': self.ativo
        }

class Estoque(db.Model):
    __tablename__ = 'estoques'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    unidade_id = db.Column(db.Integer, db.ForeignKey('unidades.id'), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False, default=0)

    # relacionamentos para facilitar as consultas entre tabelas
    unidade = db.relationship('Unidade', backref='estoques')
    produto = db.relationship('Produto', backref='estoques')

class Pedido(db.Model):
    __tablename__ = 'pedidos'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    unidade_id = db.Column(db.Integer, db.ForeignKey('unidades.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    canal_pedido = db.Column(db.Enum('APP', 'TOTEM', 'BALCAO', name='canais_enum'), nullable=False)
    status = db.Column(db.Enum('AGUARDANDO_PAGAMENTO', 'PAGO', 'EM_PREPARACAO', 'PRONTO', 'ENTREGUE', 'CANCELADO', name='status_enum'), default='AGUARDANDO_PAGAMENTO')
    forma_pagamento = db.Column(db.String(50), nullable=False)
    total = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
    criado_em = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    # vinculos relacionais do pedido
    unidade = db.relationship('Unidade')
    usuario = db.relationship('Usuario')
    itens = db.relationship('ItemPedido', backref='pedido', cascade="all, delete-orphan")

    def to_dict(self):
        return {
            'pedidoId': self.id,
            'unidadeId': self.unidade_id,
            'status': self.status,
            'canalPedido': self.canal_pedido,
            'formaPagamento': self.forma_pagamento,
            'total': float(self.total),
            'criado_em': self.criated_em.isoformat() if hasattr(self, 'criated_em') else self.criado_em.isoformat(),
            'itens': [item.to_dict() for item in self.itens]
        }

class ItemPedido(db.Model):
    __tablename__ = 'itens_pedido'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedidos.id'), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    preco_unitario = db.Column(db.Numeric(10, 2), nullable=False)

    produto = db.relationship('Produto')

    def to_dict(self):
        return {
            'produtoId': self.produto_id,
            'nome': self.produto.nome if self.produto else None,
            'quantidade': self.quantidade,
            'precoUnitario': float(self.preco_unitario)
        }