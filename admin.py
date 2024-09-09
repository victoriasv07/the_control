from flask import Blueprint, jsonify, request, render_template, redirect, url_for, flash
from flask_login import UserMixin,login_required,logout_user, LoginManager,login_user, current_user
from models.model import db, Patrimonios, Cadastro, Usuario

bp_admin = Blueprint("admin", __name__)

@bp_admin.route("/admin/home")
def admin_home():
    return render_template()

@bp_admin.route("/usuario/autorizacao", methods=["GET"])
def autorizacao_usuario_view():
    infos_usuarios = Cadastro.query.all()
    return render_template("./sistema/autorizacao_usuario.html", infos_usuarios=infos_usuarios)


    ##rota de autorização de usuario - troca de infos para outra tabela usuario
@bp_admin.route("/usuario/autorizacao/<int:id>", methods=["POST"])
def autorizacao_usuario(id):
    autorizacao_usuario_selecionado = Cadastro.query.get(id)
    
    if autorizacao_usuario_selecionado:
        usuario_autorizado = Usuario(nome=autorizacao_usuario_selecionado.nome, cpf=autorizacao_usuario_selecionado.cpf, email=autorizacao_usuario_selecionado.email, telefone=autorizacao_usuario_selecionado.telefone, mensagem=autorizacao_usuario_selecionado.mensagem)
        db.session.add(usuario_autorizado)
        db.session.commit()
        return "Usuário autorizado com sucesso e transferido"
    else:
        return "Usuário não encontrado para autorização."