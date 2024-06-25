from flask import Blueprint, jsonify, request, render_template, redirect, url_for
from flask_login import UserMixin,login_required,logout_user, LoginManager,login_user, current_user
from models.model import db, Patrimonios, Cadastro, Usuario
from sqlalchemy import select
bp_sistema = Blueprint("sistema", __name__)


@bp_sistema.route("/sistema")
def index():
    return render_template("./sistema/sistema.html")


##rota de acesso do formulário para petição de acesso ao sistema
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
    return render_template("./sistema/cadastro/cadastro.html")


##rota de visualização de usuarios por parte administrativa
@bp_sistema.route("/usuario/autorizacao", methods=["GET"])
def autorizacao_usuario_view():
    infos_usuarios = Cadastro.query.all()
    return render_template("./sistema/sistema_auth/autorizacao_usuario.html", infos_usuarios=infos_usuarios)


##rota de autorização de usuario - troca de infos para outra tabela usuario
@bp_sistema.route("/usuario/autorizacao/<int:id>", methods=["POST"])
def autorizacao_usuario(id):
    autorizacao_usuario_selecionado = Cadastro.query.get(id)
    
    if autorizacao_usuario_selecionado:
        usuario_autorizado = Usuario(nome=autorizacao_usuario_selecionado.nome, cpf=autorizacao_usuario_selecionado.cpf, email=autorizacao_usuario_selecionado.email, telefone=autorizacao_usuario_selecionado.telefone, mensagem=autorizacao_usuario_selecionado.mensagem)
        db.session.add(usuario_autorizado)
        db.session.commit()
        return "Usuário autorizado com sucesso e transferido"
    else:
        return "Usuário não encontrado para autorização."
    
@bp_sistema.route("/usuario/login", methods=["POST","GET"])
def login_usuario():
    if request.method == "POST":
        cpf = request.form.get("cpf-login")
        email = request.form.get("email-login")
        user = Usuario.query.filter_by(cpf = cpf, email = email).first()
        if user:
            return redirect(url_for("site.index"))
        else:
            return "Deu errado"
    return render_template("./sistema/login/login.html")

@bp_sistema.route("/usuario/tabela/<int:sala>", methods=["POST", "GET"])
def visualizar_patrimonio(sala):
        return "visualizar sala " + str(sala)