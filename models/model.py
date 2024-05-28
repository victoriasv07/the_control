from flask_sqlalchemy import SQLAlchemy
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

class Login(db.Model):
    __tablename__ = "login"
    id = db.Column(db.Integer, primary_key = True)
    cpf = db.Column(db.Integer, nullable = True) 
    email = db.Column(db.String(45), nullable = True) 
    token = db.Column(db.String, nullable = True) 

class Usuario(db.Model):
    __tablename__ = "usuarios "
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(45), nullable = True)
    cpf = db.Column(db.Integer, nullable = True) 
    email = db.Column(db.String(45), nullable = True) 
    telefone = db.Column(db.Integer, nullable = True) 
    mensagem = db.Column(db.Text(45), nullable = True) 