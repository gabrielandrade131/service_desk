from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Usuario(db.Model):

    __tablename__ = 'USUARIOS'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    tipo = db.Column(db.String(20), nullable=False, default='cliente')
    ativo = db.Column(db.Boolean, default=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'tipo': self.tipo,
            'ativo': self.ativo
        }


class Setor(db.Model):
    __tablename__ = 'SETORES'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False, unique=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome
        }


class Ticket(db.Model):
    __tablename__ = 'TICKETS'
    
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    prioridade = db.Column(db.String(20), nullable=False, default='Média')
    status = db.Column(db.String(20), nullable=False, default='Aberto')
    usuarios_id = db.Column(db.Integer, db.ForeignKey('USUARIOS.id'), nullable=False)
    setores_id = db.Column(db.Integer, db.ForeignKey('SETORES.id'), nullable=False)
    data_criacao = db.Column(db.DateTime, nullable=False, default=datetime.now)
    data_atualizacao = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    def to_dict(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'descricao': self.descricao,
            'prioridade': self.prioridade,
            'status': self.status,
            'usuarios_id': self.usuarios_id,
            'setores_id': self.setores_id,
            'data_criacao': self.data_criacao.isoformat() if self.data_criacao else None,
            'data_atualizacao': self.data_atualizacao.isoformat() if self.data_atualizacao else None
        }