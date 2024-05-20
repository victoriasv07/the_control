from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Patrimonios(db.Model):
    __tablename__ = "infos"
    id = db.Column(db.Integer, primary_key = True)
    descricao = db.Column(db.String(100), nullable = False)
    categoria = db.Column(db.String(100), nullable = False)