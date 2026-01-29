from flask import Blueprint, request, jsonify
from models import db, Ticket, Setor, Usuario
from datetime import datetime

tickets_bp = Blueprint('tickets', __name__, url_prefix='/api/tickets')


@tickets_bp.route('', methods=['GET'])
def get_all_tickets():
    try:
        setor_id = request.args.get('setor_id')
        prioridade = request.args.get('prioridade')
        status = request.args.get('status')
        
        query = Ticket.query
        
        if setor_id:
            query = query.filter_by(setores_id=setor_id)
        
        if prioridade:
            query = query.filter_by(prioridade=prioridade)
        
        if status:
            query = query.filter_by(status=status)
        
        tickets = query.all()
        
        if not tickets:
            return jsonify({'mensagem': 'Nenhum ticket encontrado'}), 404
        
        return jsonify({
            'quantidade': len(tickets),
            'tickets': [ticket.to_dict() for ticket in tickets]
        }), 200
    
    except Exception as e:
        return jsonify({'erro': str(e)}), 500



@tickets_bp.route('/<int:id>', methods=['GET'])
def get_ticket_by_id(id):
    try:
        ticket = Ticket.query.get(id)
        
        if not ticket:
            return jsonify({'erro': f'Ticket {id} não encontrado'}), 404
        
        return jsonify(ticket.to_dict()), 200
    
    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@tickets_bp.route('', methods=['POST'])
def create_ticket():
    try:
        data = request.get_json()
        
        if not data.get('titulo'):
            return jsonify({'erro': 'Campo "titulo" é obrigatório'}), 400
        
        if not data.get('descricao'):
            return jsonify({'erro': 'Campo "descricao" é obrigatório'}), 400
        
        if not data.get('usuarios_id'):
            return jsonify({'erro': 'Campo "usuarios_id" é obrigatório'}), 400
        
        if not data.get('setores_id'):
            return jsonify({'erro': 'Campo "setores_id" é obrigatório'}), 400
        
        usuario = Usuario.query.get(data.get('usuarios_id'))
        if not usuario:
            return jsonify({'erro': 'Usuário não encontrado'}), 404
        
        setor = Setor.query.get(data.get('setores_id'))
        if not setor:
            return jsonify({'erro': 'Setor não encontrado'}), 404
        
        novo_ticket = Ticket(
            titulo=data.get('titulo'),
            descricao=data.get('descricao'),
            prioridade=data.get('prioridade', 'Média'),
            status=data.get('status', 'Aberto'),
            usuarios_id=data.get('usuarios_id'),
            setores_id=data.get('setores_id')
        )
        
        db.session.add(novo_ticket)
        db.session.commit()
        
        return jsonify({
            'mensagem': 'Ticket criado com sucesso',
            'ticket': novo_ticket.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500


@tickets_bp.route('/<int:id>', methods=['PUT'])
def update_ticket(id):
    try:
        ticket = Ticket.query.get(id)
        
        if not ticket:
            return jsonify({'erro': f'Ticket {id} não encontrado'}), 404
        
        data = request.get_json()
        
        if 'titulo' in data:
            ticket.titulo = data['titulo']
        
        if 'descricao' in data:
            ticket.descricao = data['descricao']
        
        if 'prioridade' in data:
            ticket.prioridade = data['prioridade']
        
        if 'status' in data:
            ticket.status = data['status']
        
        if 'usuarios_id' in data:
            usuario = Usuario.query.get(data['usuarios_id'])
            if not usuario:
                return jsonify({'erro': 'Usuário não encontrado'}), 404
            ticket.usuarios_id = data['usuarios_id']
        
        if 'setores_id' in data:
            setor = Setor.query.get(data['setores_id'])
            if not setor:
                return jsonify({'erro': 'Setor não encontrado'}), 404
            ticket.setores_id = data['setores_id']
        
        ticket.data_atualizacao = datetime.now()
        
        db.session.commit()
        
        return jsonify({
            'mensagem': 'Ticket atualizado com sucesso',
            'ticket': ticket.to_dict()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500


@tickets_bp.route('/<int:id>', methods=['DELETE'])
def delete_ticket(id):
    try:
        ticket = Ticket.query.get(id)
        
        if not ticket:
            return jsonify({'erro': f'Ticket {id} não encontrado'}), 404
        
        db.session.delete(ticket)
        db.session.commit()
        
        return jsonify({
            'mensagem': f'Ticket {id} deletado com sucesso'
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500