from app.infrastructure.database import db
from app.domain.models import Unidade, Produto, Estoque

UNIDADE_PADRAO = {'nome': 'Unidade Paraty', 'cidade': 'Paraty'}

PRODUTOS_PADRAO = (
    {'id': 101, 'nome': 'Tapioca de Carne de Sol', 'preco': 18.50},
    {'id': 305, 'nome': 'Suco de Graviola 400ml', 'preco': 8.00},
)

ESTOQUE_INICIAL = 50


def popular_dados_iniciais():
    unidade = Unidade.query.filter_by(nome=UNIDADE_PADRAO['nome']).first()
    if unidade is None:
        unidade = Unidade(**UNIDADE_PADRAO)
        db.session.add(unidade)
        db.session.flush()

    for dados in PRODUTOS_PADRAO:
        produto = Produto.query.get(dados['id'])
        if produto is None:
            produto = Produto(**dados)
            db.session.add(produto)
            db.session.flush()

        estoque = Estoque.query.filter_by(unidade_id=unidade.id, produto_id=produto.id).first()
        if estoque is None:
            db.session.add(
                Estoque(unidade_id=unidade.id, produto_id=produto.id, quantidade=ESTOQUE_INICIAL)
            )

    db.session.commit()
    return unidade
