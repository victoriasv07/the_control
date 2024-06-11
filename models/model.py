from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
db = SQLAlchemy()

class Patrimonios(db.Model):
    __tablename__ = "patrimonios"
    id = db.Column(db.Integer, primary_key = True)
    descricao = db.Column(db.String(100), nullable = False)
    categoria = db.Column(db.String(100), nullable = False)

class Cadastro(db.Model):
    __tablename__ = "cadastro_usuario"
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(45), nullable = True)
    cpf = db.Column(db.Integer, nullable = True) 
    email = db.Column(db.String(45), nullable = True) 
    telefone = db.Column(db.Integer, nullable = True) 
    mensagem = db.Column(db.Text(45), nullable = True) 


class Usuario(db.Model, UserMixin):
    __tablename__ = "usuario"
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(45), nullable = True)
    cpf = db.Column(db.Integer, nullable = True) 
    email = db.Column(db.String(45), nullable = True) 
    telefone = db.Column(db.Integer, nullable = True) 
    mensagem = db.Column(db.Text(45), nullable = True)
    def check_email(self, cpf):
        return cpf    