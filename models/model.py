from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Usuario(db.Model, UserMixin):
    __tablename__ = "usuario"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(45), nullable=True)
    cpf = db.Column(db.String(11), nullable=True)  
    email = db.Column(db.String(45), nullable=True)
    telefone = db.Column(db.String(15), nullable=True) 
    password = db.Column(db.String(128), nullable=False)

class Admin(db.Model, UserMixin):
    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=True)
    cpf = db.Column(db.String(11), nullable=True)

class Patrimonios(db.Model):
    __tablename__ = "patrimonios"
    id = db.Column(db.Integer, primary_key=True)
    numero_de_etiqueta = db.Column(db.String(100), nullable=False)
    denominacao_de_imobiliario = db.Column(db.String(100), nullable=False)
    data_de_chegada = db.Column(db.String(100), nullable=False)
    local = db.Column(db.String(100), nullable=False)

class Cadastro(db.Model):
    __tablename__ = "cadastro_usuario"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(45), nullable=True)
    cpf = db.Column(db.String(11), nullable=True)  
    email = db.Column(db.String(45), nullable=True)
    telefone = db.Column(db.String(15), nullable=True) 
    mensagem = db.Column(db.Text, nullable=True)
