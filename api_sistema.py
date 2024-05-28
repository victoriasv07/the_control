from flask import Blueprint, jsonify, request, render_template, redirect
from models.model import db, Patrimonios, Cadastro, Usuario
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

# @bp_sistema.route("/usuarios/acesso", methods=["POST", "GET"])
# def login_acesso():
#     if request.method == "POST":
#         token = request.form.get ('token')
#         cpf = request.form.get ('cpf')
#         email = request.form.get ('email')


@bp_sistema.route("/usuario/autorizacao", methods=["GET"])
def autorizacao_usuario_view():
    infos_usuarios = Cadastro.query.all()
    return render_template("./sistema/sistema_auth/autorizacao_usuario.html", infos_usuarios=infos_usuarios)

@bp_sistema.route("/usuario/autorizacao/<int:id>", methods=["POST"])
def autorizacao_usuario(id):
    autorizacao_usuario_selecionado = Cadastro.query.get(id)
    
    if autorizacao_usuario_selecionado:
        usuario_autorizado = Usuario(nome=autorizacao_usuario_selecionado.nome, cpf=autorizacao_usuario_selecionado.cpf, email=autorizacao_usuario_selecionado.email, telefone=autorizacao_usuario_selecionado.telefone, mensagem=autorizacao_usuario_selecionado.mensagem)
        db.session.add(usuario_autorizado)
        db.session.commit()
        
        return "Usuário autorizado com sucesso!"
    else:
        return "Usuário não encontrado para autorização."