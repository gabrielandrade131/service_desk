from flask import Blueprint, request, jsonify
from models import db, Usuario

usuarios_bp = Blueprint('usuarios', __name__, url_prefix='/api/usuarios')


@usuarios_bp.route('', methods=['GET'])
def get_all_usuarios():
    try:
        usuarios = Usuario.query.all()
        
        if not usuarios:
            return jsonify({'mensagem': 'Nenhum usuário encontrado'}), 404
        
        return jsonify({
            'quantidade': len(usuarios),
            'usuarios': [usuario.to_dict() for usuario in usuarios]
        }), 200
    
    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@usuarios_bp.route('/<int:id>', methods=['GET'])
def get_usuario_by_id(id):
    try:
        usuario = Usuario.query.get(id)
        
        if not usuario:
            return jsonify({'erro': f'Usuário {id} não encontrado'}), 404
        
        return jsonify(usuario.to_dict()), 200
    
    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@usuarios_bp.route('', methods=['POST'])
def create_usuario():
    try:
        data = request.get_json()
        
        if not data.get('nome'):
            return jsonify({'erro': 'Campo "nome" é obrigatório'}), 400
        
        if not data.get('email'):
            return jsonify({'erro': 'Campo "email" é obrigatório'}), 400
        
        usuario_existente = Usuario.query.filter_by(email=data.get('email')).first()
        if usuario_existente:
            return jsonify({'erro': 'Email já cadastrado'}), 400
        
        novo_usuario = Usuario(
            nome=data.get('nome'),
            email=data.get('email'),
            tipo=data.get('tipo', 'cliente'),
            ativo=data.get('ativo', True)
        )
        
        db.session.add(novo_usuario)
        db.session.commit()
        
        return jsonify({
            'mensagem': 'Usuário criado com sucesso',
            'usuario': novo_usuario.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500


@usuarios_bp.route('/<int:id>', methods=['PUT'])
def update_usuario(id):
    try:
        usuario = Usuario.query.get(id)
        
        if not usuario:
            return jsonify({'erro': f'Usuário {id} não encontrado'}), 404
        
        data = request.get_json()
        
        if 'nome' in data:
            usuario.nome = data['nome']
        
        if 'email' in data:
            usuario_existente = Usuario.query.filter_by(email=data['email']).first()
            if usuario_existente and usuario_existente.id != id:
                return jsonify({'erro': 'Email já cadastrado'}), 400
            usuario.email = data['email']
        
        if 'tipo' in data:
            usuario.tipo = data['tipo']
        
        if 'ativo' in data:
            usuario.ativo = data['ativo']
        
        db.session.commit()
        
        return jsonify({
            'mensagem': 'Usuário atualizado com sucesso',
            'usuario': usuario.to_dict()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500


@usuarios_bp.route('/<int:id>', methods=['DELETE'])
def delete_usuario(id):
    try:
        usuario = Usuario.query.get(id)
        
        if not usuario:
            return jsonify({'erro': f'Usuário {id} não encontrado'}), 404
        
        db.session.delete(usuario)
        db.session.commit()
        
        return jsonify({
            'mensagem': f'Usuário {id} deletado com sucesso'
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500