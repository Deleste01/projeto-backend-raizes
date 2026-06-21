from flask import Blueprint, request, jsonify
from app.infrastructure.database import db
from app.domain.models import Pedido, ItemPedido, Produto, Estoque
from app.auth import login_required, roles_accepted
import datetime

pedidos_bp = Blueprint('pedidos', __name__, url_prefix='/api')

@pedidos_bp.route('/pedidos', methods=['POST'])
@login_required
@roles_accepted('funcionario', 'cliente')
def criar_pedido(current_user):
    # Rota principal para fazer o pedido, valida estoque e calcula o valor final
    req_data = request.get_json() or {}
    
    unidade_id = req_data.get('unidadeId')
    itens_request = req_data.get('itens', [])
    forma_pagamento = req_data.get('formaPagamento')
    canal_pedido = req_data.get('canalPedido')  # <-- CORRECAO HUMANA: Arrancamos o 'BALCAO' automatico

    # Dominio multi-canal oficial da Rede Raizes do Nordeste
    canais_permitidos = ['APP', 'TOTEM', 'BALCAO', 'PICKUP', 'WEB']

    if not unidade_id or not itens_request or not forma_pagamento or not canal_pedido:
        return jsonify({'error': 'DADOS_INVALIDOS', 'message': 'Campos obrigatorios ausentes (unidadeId, itens, formaPagamento ou canalPedido).'}), 422

    if canal_pedido not in canais_permitidos:
        return jsonify({
            'error': 'CANAL_INVALIDO', 
            'message': f'Canal de pedido invalido. Aceitos: {canais_permitidos}'
        }), 422

    total_acumulado = 0
    lista_itens_novos = []

    try:
        for item in itens_request:
            prod_id = item.get('produtoId')
            qtd = item.get('quantidade')

            if not prod_id or not qtd or qtd <= 0:
                return jsonify({'error': 'ITEM_INVALIDO', 'message': 'Produto ou quantidade inválida.'}), 422

            prod_obj = Produto.query.get(prod_id)
            if not prod_obj:
                return jsonify({'error': 'PRODUTO_NAO_ENCONTRADO', 'message': f'Produto ID {prod_id} não existe.'}), 404

            # Verifica se tem o produto em estoque na unidade correta
            item_estoque = Estoque.query.filter_by(unidade_id=unidade_id, produto_id=prod_id).first()
            if not item_estoque or item_estoque.quantidade < qtd:
                return jsonify({
                    'error': 'ESTOQUE_INSUFICIENTE', 
                    'message': f'Estoque insuficiente para o produto {prod_obj.nome}.'
                }), 422

            preco_atual = prod_obj.preco
            total_acumulado += (preco_atual * qtd)

            # Baixa a quantidade do estoque da unidade física
            item_estoque.quantidade -= qtd

            novo_item = ItemPedido(
                produto_id=prod_id,
                quantidade=qtd,
                preco_unitario=preco_atual
            )
            lista_itens_novos.append(novo_item)

        pedido_obj = Pedido(
            unidade_id=unidade_id,
            usuario_id=current_user.id,  
            canal_pedido=canal_pedido,
            status='AGUARDANDO_PAGAMENTO',
            forma_pagamento=forma_pagamento,
            total=total_acumulado
        )

        for item_salvar in lista_itens_novos:
            pedido_obj.itens.append(item_salvar)

        db.session.add(pedido_obj)
        db.session.commit()

        return jsonify(pedido_obj.to_dict()), 201

    except Exception as erro:
        db.session.rollback()
        return jsonify({'error': 'ERRO_INTERNO', 'message': str(erro)}), 500


@pedidos_bp.route('/pedidos/<int:pedido_id>/pagar', methods=['POST'])
@login_required
@roles_accepted('funcionario')
def pagar_pedido(current_user, pedido_id):
    # Simula o pagamento recebido pelo sistema de caixa (mock)
    ped = Pedido.query.get(pedido_id)
    
    if not ped:
        return jsonify({'error': 'PEDIDO_NAO_ENCONTRADO', 'message': 'Pedido não encontrado.'}), 404
        
    if ped.status != 'AGUARDANDO_PAGAMENTO':
        return jsonify({'error': 'STATUS_INVALIDO', 'message': 'Este pedido já foi pago ou cancelado.'}), 400

    try:
        ped.status = 'PAGO'
        db.session.commit()
        
        return jsonify({
            'mensagem': 'Pagamento processado com sucesso (Simulação Mock)!',
            'pedidoId': ped.id,
            'status': ped.status
        }), 200
        
    except Exception as erro:
        db.session.rollback()
        return jsonify({'error': 'ERRO_INTERNO', 'message': str(erro)}), 500


@pedidos_bp.route('/pedidos/<int:pedido_id>/status', methods=['PATCH'])
@login_required
@roles_accepted('funcionario')
def atualizar_status(current_user, pedido_id):
    # Rota para avancar o status do pedido na linha de producao da lanchonete
    req_data = request.get_json() or {}
    novo_status = req_data.get('status')
    
    status_permitidos = ['EM_PREPARACAO', 'PRONTO', 'ENTREGUE', 'CANCELADO']
    
    if novo_status not in status_permitidos:
        return jsonify({'error': 'STATUS_INVALIDO', 'message': f'Status deve ser um dos seguintes: {status_permitidos}'}), 400
        
    ped = Pedido.query.get(pedido_id)
    if not ped:
        return jsonify({'error': 'PEDIDO_NAO_ENCONTRADO', 'message': 'Pedido não encontrado.'}), 404

    try:
        ped.status = novo_status
        db.session.commit()
        
        return jsonify({
            'mensagem': 'Status do pedido atualizado com sucesso!',
            'pedidoId': ped.id,
            'status': ped.status
        }), 200
        
    except Exception as erro:
        db.session.rollback()
        return jsonify({'error': 'ERRO_INTERNO', 'message': str(erro)}), 500