from flask import Blueprint, request, jsonify
from models import db, Setor

setores_bp = Blueprint('setores', __name__, url_prefix='/api/setores')


@setores_bp.route('', methods=['GET'])
def get_all_setores():
    try:
        setores = Setor.query.all()
        
        if not setores:
            return jsonify({'mensagem': 'Nenhum setor encontrado'}), 404
        
        return jsonify({
            'quantidade': len(setores),
            'setores': [setor.to_dict() for setor in setores]
        }), 200
    
    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@setores_bp.route('/<int:id>', methods=['GET'])
def get_setor_by_id(id):
    try:
        setor = Setor.query.get(id)
        
        if not setor:
            return jsonify({'erro': f'Setor {id} não encontrado'}), 404
        
        return jsonify(setor.to_dict()), 200
    
    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@setores_bp.route('', methods=['POST'])
def create_setor():
    try:
        data = request.get_json()
        
        if not data.get('nome'):
            return jsonify({'erro': 'Campo "nome" é obrigatório'}), 400
        
        setor_existente = Setor.query.filter_by(nome=data.get('nome')).first()
        if setor_existente:
            return jsonify({'erro': 'Setor já existe'}), 400
        
        novo_setor = Setor(
            nome=data.get('nome')
        )
        
        db.session.add(novo_setor)
        db.session.commit()
        
        return jsonify({
            'mensagem': 'Setor criado com sucesso',
            'setor': novo_setor.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500


@setores_bp.route('/<int:id>', methods=['PUT'])
def update_setor(id):
    try:
        setor = Setor.query.get(id)
        
        if not setor:
            return jsonify({'erro': f'Setor {id} não encontrado'}), 404
        
        data = request.get_json()
        
        if 'nome' in data:
            setor_existente = Setor.query.filter_by(nome=data['nome']).first()
            if setor_existente and setor_existente.id != id:
                return jsonify({'erro': 'Setor já existe'}), 400
            setor.nome = data['nome']
        
        db.session.commit()
        
        return jsonify({
            'mensagem': 'Setor atualizado com sucesso',
            'setor': setor.to_dict()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500


@setores_bp.route('/<int:id>', methods=['DELETE'])
def delete_setor(id):
    try:
        setor = Setor.query.get(id)
        
        if not setor:
            return jsonify({'erro': f'Setor {id} não encontrado'}), 404
        
        db.session.delete(setor)
        db.session.commit()
        
        return jsonify({
            'mensagem': f'Setor {id} deletado com sucesso'
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500