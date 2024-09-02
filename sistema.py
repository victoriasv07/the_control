from flask import Blueprint, jsonify, request, render_template, redirect, url_for, flash
from flask_login import UserMixin,login_required,logout_user, LoginManager,login_user, current_user
from models.model import db, Patrimonios, Cadastro, Usuario

bp_sistema = Blueprint("sistema", __name__)


##rota base sistemas
@bp_sistema.route("/sistema")
def index():
    return render_template("./sistema/layout.html")

#teste de funcionalidade de camera
@bp_sistema.route("/camera")
def mostrar_camera():
    return render_template("./sistema/camera.html")


##rota de acesso do formulário para petição de acesso ao sistema
@bp_sistema.route("/register", methods=["POST", "GET"])
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
    return render_template("./sistema/cadastro.html")


##rota de visualização de usuarios por parte administrativa
@bp_sistema.route("/usuario/autorizacao", methods=["GET"])
def autorizacao_usuario_view():
    infos_usuarios = Cadastro.query.all()
    return render_template("./sistema/autorizacao_usuario.html", infos_usuarios=infos_usuarios)


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

##rota de login usuario
@bp_sistema.route("/login", methods=["POST","GET"])
def login_usuario():
    if request.method == "POST":
        cpf = request.form.get("cpf-login")
        email = request.form.get("email-login")
        user = Usuario.query.filter_by(cpf = cpf, email = email).first()
        if user:
            login_user(user)
            return redirect(url_for("site.index"))
        else:
            return "Deu errado"
    return render_template("./sistema/login.html")

#rota para filtrar salas a partir da navbar
@bp_sistema.route("/filtrar", methods=["POST", "GET"])
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
@bp_sistema.route("/deletar", methods=["POST"])
def deletar_patrimonio():
    patrimonio_id = request.form.get('patrimonio_id')
    patrimonio = Patrimonios.query.get(patrimonio_id)
    if patrimonio:
        db.session.delete(patrimonio)
        db.session.commit()
        return redirect(url_for('sistema.visualizar_patrimonio'))
    else:
        return'Patrimônio não encontrado'


##rota para atualizar patrimônios
@bp_sistema.route("/atualizar", methods=["POST"])
def atualizar_patrimonio():
    patrimonio_id = request.form.get('patrimonio_id')
    patrimonio = Patrimonios.query.get(patrimonio_id)
    if patrimonio:
        return 'patrimonio atualizado'
    else:
        return 'none'
    