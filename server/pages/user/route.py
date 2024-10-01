from flask import Blueprint, jsonify, request, render_template, redirect, url_for, flash, session
from flask_login import login_required, logout_user, login_user, current_user
from models.model import db, Patrimonios, Cadastro, Usuario, Admin

bp_user = Blueprint("user", __name__)

##rota base sistemas
@bp_user.route("/sistema")
@login_required
def index():
    return render_template("./sistema/user/layout.html")

@bp_user.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('user.login_usuario'))

##rota de login usuario
@bp_user.route("/login", methods=["POST", "GET"])
def login_usuario():
    message = None
    if request.method == "POST":
        cpf = request.form.get("cpf")
        email = request.form.get("email")
        user = Usuario.query.filter_by(cpf=cpf, email=email).first()
        admin = Admin.query.filter_by(cpf=cpf, email = email).first()
        if user:
            login_user(user)
            return redirect(url_for("user.index"))
        if admin:
            login_user(admin)
            return redirect(url_for("admin.admin_home"))
        else:
            message = "email, senha ou token inválidos"
            return 
    return render_template("./sistema/login.html", message = message)


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
        return redirect(url_for("login_usuario"))
    return render_template("./sistema/cadastro.html")

#rota para filtrar salas a partir da navbar
@bp_user.route("/filtrar", methods=["POST", "GET"])
@login_required
def visualizar_patrimonio():
    sala = request.args.get("sala")
    if sala is None:
        ##Nenhum parâmetro de sala fornecido.
        patrimonios = Patrimonios.query.all()
    else:
        try:
            sala_inteiro = int(sala)  
            patrimonios = Patrimonios.query.filter_by(local=sala_inteiro).all()
        except ValueError:
            patrimonios = Patrimonios.query.filter_by(local=sala).all()

    return render_template("./sistema/user/layout.html", patrimonios=patrimonios, sala = sala)

# Rota de deletar patrimônio
@bp_user.route("/deletar", methods=["POST"])
@login_required
def deletar_patrimonio():
    message = ""
    patrimonio_id = request.form.get('patrimonio_id')
    if not patrimonio_id:
        return 'ID do patrimônio não fornecido', 400
    
    patrimonio = Patrimonios.query.get(patrimonio_id)
    if patrimonio:
        db.session.delete(patrimonio)
        db.session.commit()
        ##Patrimônio deletado 
        return redirect(url_for('user.visualizar_patrimonio'))
    else:
        flash('Patrimônio não encontrado', 'error')
        return redirect(url_for('user.visualizar_patrimonio'))

# Rota para atualizar patrimônio
@bp_user.route("/atualizar", methods=["POST"])
@login_required
def atualizar_patrimonio():
    patrimonio_id = request.form.get('patrimonio_id')
    novo_valor = request.form.get('novo_valor') 

    if not patrimonio_id or not novo_valor:
        flash('Dados insuficientes para atualização', 'error')
        return redirect(url_for('user.visualizar_patrimonio'))

    patrimonio = Patrimonios.query.get(patrimonio_id)
    if patrimonio:
        patrimonio.denominacao_de_imobiliario = novo_valor
        db.session.commit()
        #Patrimônio atualizado 
        return redirect(url_for('user.visualizar_patrimonio'))
    else:
        #Patrimônio não encontrado
        return redirect(url_for('user.visualizar_patrimonio'))
    
@bp_user.route("/criar", methods =["POST"])
@login_required
def criar_patrimonio():
    pass

#teste de funcionalidade de camera
@bp_user.route("/camera")
def mostrar_camera():
    return render_template("./sistema/camera.html")
