from flask import Blueprint, request, jsonify, current_app
from app.infrastructure.database import db       
from app.domain.models import Usuario            
import jwt
import datetime
from functools import wraps

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

def login_required(f):
    # Interceptador para validar o token JWT nas rotas protegidas
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]

        if not token:
            return jsonify({'error': 'TOKEN_AUSENTE', 'message': 'Token de autenticação não fornecido.'}), 401

        try:
            # Descriptografa o token com a chave do app
            payload = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
            user_logado = Usuario.query.get(payload['usuario_id'])
            
            if not user_logado:
                return jsonify({'error': 'USUARIO_INVALIDO', 'message': 'Usuário associado ao token não existe.'}), 401
                
            if not user_logado.ativo:
                return jsonify({'error': 'USUARIO_INATIVO', 'message': 'Este usuário está inativo no sistema.'}), 403
                
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'TOKEN_EXPIRADO', 'message': 'O token fornecido expirou.'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'TOKEN_INVALIDO', 'message': 'Token inválido ou corrompido.'}), 401

        # Manda o objeto do usuario adiante na rota
        return f(user_logado, *args, **kwargs)

    return decorated


def roles_accepted(*perfis_permitidos):
    # Verifica o nivel de permissao (role) do usuario
    def decorator(f):
        @wraps(f)
        def decorated_function(user_logado, *args, **kwargs):
            if user_logado.role not in perfis_permitidos:
                return jsonify({
                    'error': 'ACESSO_NEGADO', 
                    'message': f'Acesso restrito para os perfis: {list(perfis_permitidos)}.'
                }), 403
            return f(user_logado, *args, **kwargs)
        return decorated_function
    return decorator


@auth_bp.route('/register', methods=['POST'])
def register():
    # Rota para cadastrar novos funcionarios ou clientes
    req_data = request.get_json() or {}
    
    if 'nome' not in req_data or 'email' not in req_data or 'senha' not in req_data:
        return jsonify({'erro': 'Campos obrigatórios ausentes (nome, email, senha)'}), 400
        
    if Usuario.query.filter_by(email=req_data['email']).first():
        return jsonify({'erro': 'Este e-mail já está cadastrado'}), 400
        
    try:
        novo = Usuario(
            nome=req_data['nome'],
            email=req_data['email']
        )
        novo.set_senha(req_data['senha'])
        
        db.session.add(novo)
        db.session.commit()
        
        return jsonify({
            'mensagem': 'Usuário cadastrado com sucesso!',
            'usuario': novo.to_dict()
        }), 201
        
    except Exception as erro:
        db.session.rollback()
        return jsonify({'erro': 'Erro interno ao salvar no banco', 'detalhe': str(erro)}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    # Valida as credenciais e devolve o token de acesso
    req_data = request.get_json() or {}
    
    if 'email' not in req_data or 'senha' not in req_data:
        return jsonify({'erro': 'E-mail e senha são obrigatórios'}), 400
        
    user = Usuario.query.filter_by(email=req_data['email']).first()
    
    if not user or not user.verificar_senha(req_data['senha']):
        return jsonify({'erro': 'E-mail ou senha inválidos'}), 401
        
    # Gera o token com duracao de 24h
    access_token = jwt.encode({
        'usuario_id': user.id,
        'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=24)
    }, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')
    
    return jsonify({
        'mensagem': 'Login realizado com sucesso!',
        'token': access_token,
        'usuario': user.to_dict()
    }), 200