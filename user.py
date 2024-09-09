from flask import Blueprint, jsonify, request, render_template, redirect, url_for, flash, session
from flask_login import login_required, logout_user, login_user, current_user
from models.model import db, Patrimonios, Cadastro, Usuario, Admin

bp_user = Blueprint("user", __name__)

##rota base sistemas
@bp_user.route("/sistema")
def index():
    return render_template("./sistema/layout.html")

##rota de login usuario
@bp_user.route("/login", methods=["POST", "GET"])
def login_usuario():
    if request.method == "POST":
        cpf = request.form.get("cpf")
        email = request.form.get("email")
        user = Usuario.query.filter_by(cpf=cpf, email=email).first()
        admin = Admin.query.filter_by(cpf=cpf, email = email).first()
        if user:
            return redirect(url_for("user.index"))
        if admin:
            return redirect(url_for("./admin/admin_home.html"))
        else:
            return "Deu errado"
    return render_template("./sistema/login.html")


##rota de acesso do formulário para petição de acesso ao sistema
@bp_user.route("/register", methods=["POST", "GET"])
def forms_acesso():
    if request.method == "POST":
        nome = request.form.get('nome')
        cpf = request.form.get('cpf')
        telefone = request.form.get('telefone')
        email = request.form.get('email')
        mensagem = request.form.get('mensagem')
        novo_usuario = Cadastro(nome=nome, cpf=cpf, telefone=telefone, email=email, mensagem=mensagem)
        db.session.add(novo_usuario)
        db.session.commit()
        return "Concluido"
    return render_template("./sistema/cadastro.html")

#rota para filtrar salas a partir da navbar
@bp_user.route("/filtrar", methods=["POST", "GET"])
def visualizar_patrimonio():
    sala = request.args.get("sala")
    if sala is None:
        return "Erro: parâmetro sala não fornecido", 400
    try:
        sala_inteiro = int(sala)
        patrimonios = Patrimonios.query.filter_by(local=sala_inteiro).all()
    except ValueError:
        patrimonios = Patrimonios.query.filter_by(local=sala).all()

    return render_template("./sistema/patrimonios.html", patrimonios=patrimonios)

##rota de deletar patrimonios do usuario
@bp_user.route("/deletar", methods=["POST"])
def deletar_patrimonio():
    patrimonio_id = request.form.get('patrimonio_id')
    patrimonio = Patrimonios.query.get(patrimonio_id)
    if patrimonio:
        db.session.delete(patrimonio)
        db.session.commit()
        return redirect(url_for('user.visualizar_patrimonio'))
    else:
        return 'Patrimônio não encontrado'

##rota para atualizar patrimônios
@bp_user.route("/atualizar", methods=["POST"])
def atualizar_patrimonio():
    patrimonio_id = request.form.get('patrimonio_id')
    patrimonio = Patrimonios.query.get(patrimonio_id)
    if patrimonio:
        return 'patrimonio atualizado'
    else:
        return 'none'

#teste de funcionalidade de camera
@bp_user.route("/camera")
def mostrar_camera():
    return render_template("./sistema/camera.html")
