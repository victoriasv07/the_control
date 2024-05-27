from flask import Blueprint, jsonify, request, render_template, redirect
from models.model import db, Patrimonios, Cadastro
bp_sistema = Blueprint("sistema", __name__)

@bp_sistema.route("/sistema")
def index():
    return render_template("./sistema/sistema.html")

@bp_sistema.route("/forms/acesso", methods=["POST", "GET"])
def forms_acesso():
    if request.method == "POST":
        nome = request.form.get ('nome')
        cpf = request.form.get ('cpf')
        telefone = request.form.get ('telefone') 
        email = request.form.get ('email')
        mensagem = request.form.get ('mensagem')  
        novo_usuario = Cadastro(nome=nome, cpf=cpf, telefone=telefone, email=email, mensagem=mensagem)
        db.session.add(novo_usuario)
        db.session.commit()
        return "Concluido"
    return render_template("./sistema/registro/form_usuario.html")

@bp_sistema.route("/usuarios/acesso", methods=["POST", "GET"])
def login_acesso():
    if request.method == "POST":
        token = request.form.get ('token')
        cpf = request.form.get ('cpf')
        email = request.form.get ('email')
         

@bp_sistema.route("/usuario/autorizacao/usuario", methods = ["POST", "GET"])
def autorizacao_usuario():
    infos_usuarios = Cadastro.query.all()
    return render_template("./sistema/sistema_auth/autorizacao_usuario.html", infos_usuarios = infos_usuarios)