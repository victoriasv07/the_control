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
    """
    Essa rota é responsável por fazer logout do usuário no sistema.

    Ela chama o método logout_user() da biblioteca Flask-Login,
    que remove a sess o do usu rio e o desloga do sistema.
    Em seguida, redireciona o usu rio para a p gina de login.
    """
    logout_user()
    return redirect(url_for('user.login_usuario'))



##rota de login usuario
@bp_user.route("/login", methods=["POST", "GET"])
def login_usuario():
    """
    Essa rota é responsável pelo login do usuário no sistema.

    Se o método for GET, retorna a página de login.
    Se o método for POST, verifica se o CPF e o email estão corretos,
    e se sim, loga o usuário no sistema.
    """
    message = None
    if request.method == "POST":
        cpf = request.form.get("cpf")
        email = request.form.get("email")
        # Verifica se o CPF e o email estão corretos
        user = Usuario.query.filter_by(cpf=cpf, email=email).first()
        admin = Admin.query.filter_by(cpf=cpf, email=email).first()
        if user:
            # Se o usuário for encontrado, loga o usuário no sistema
            login_user(user)
            return redirect(url_for("user.index"))
        if admin:
            # Se o administrador for encontrado, loga o administrador no sistema
            login_user(admin)
            return redirect(url_for("admin.admin_home"))
        else:
            # Se o usuário ou o administrador não forem encontrados, retorna uma mensagem de erro
            message = "email, senha ou token inválidos"
            return render_template("./sistema/login.html", message=message)
    # Se o método for GET, retorna a página de login
    return render_template("./sistema/login.html", message=message)
##rota de acesso do formulário para petição de acesso ao sistema


@bp_user.route("/register", methods=["POST", "GET"])
def forms_acesso():
    """
    Essa rota é responsável pelo cadastro de usuários no sistema.

    Se o método for GET, retorna o formulário de cadastro.
    Se o método for POST, faz o cadastro do usuário no banco de dados.
    """
    if request.method == "POST":
        # Pegar os dados do formulário
        nome = request.form.get('nome')
        cpf = request.form.get('cpf')
        telefone = request.form.get('telefone')
        email = request.form.get('email')
        mensagem = request.form.get('mensagem')

        # Criar um novo usuário
        novo_usuario = Cadastro(nome=nome, cpf=cpf, telefone=telefone, email=email, mensagem=mensagem)

        # Adicionar o novo usuário ao banco de dados
        db.session.add(novo_usuario)
        db.session.commit()

        # Redirecionar para a página de login
        return redirect(url_for("login_usuario"))

    # Se o método for GET, retorna o formulário de cadastro
    return render_template("./sistema/cadastro.html")

#rota para filtrar salas a partir da navbar



@bp_user.route("/filtrar", methods=["POST", "GET"])
@login_required
def visualizar_patrimonio():
    """
    Essa rota é responsável por filtrar patrimônios por sala.

    Se o parâmetro "sala" for fornecido, ele filtra os patrimônios por essa sala.
    Caso contrário, ele retorna todos os patrimônios.
    """
    sala = request.args.get("sala")
    if sala is None:
        ##Nenhum parâmetro de sala fornecido.
        patrimonios = Patrimonios.query.all()
    else:
        try:
            # Tenta converter o parâmetro de sala para inteiro
            sala_inteiro = int(sala)  
            # Filtra os patrimônios por sala
            patrimonios = Patrimonios.query.filter_by(local=sala_inteiro).all()
        except ValueError:
            # Se o parâmetro de sala não for um inteiro, filtra por string
            patrimonios = Patrimonios.query.filter_by(local=sala).all()

    # Retorna os patrimônios filtrados
    return render_template("./sistema/user/layout.html", patrimonios=patrimonios, sala = sala)



# Rota de deletar patrimônio
@bp_user.route("/deletar", methods=["POST"])
@login_required
def deletar_patrimonio():
    """
    Essa rota deleta um patrimônio do banco de dados.

    Ela recebe o ID do patrimônio a ser deletado como um parâmetro
    na requisição. Se o ID for fornecido, ele deleta o patrimônio
    do banco de dados e retorna a página de patrimônios.

    Se o ID não for fornecido, ele retorna um erro 400.
    Se o patrimônio não for encontrado, ele retorna um erro 404.
    """
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
    """
    Essa rota atualiza um patrimônio no banco de dados.

    Ela recebe o ID do patrimônio a ser atualizado e o
    novo valor para o campo "denominacao_de_imobiliario"
    como parâmetros na requisição. Se os parâmetros forem
    fornecidos, ele atualiza o patrimônio no banco de dados
    e retorna a página de patrimônios.

    Se os parâmetros não forem fornecidos, ele retorna um
    erro 400. Se o patrimônio não for encontrado, ele retorna
    um erro 404.
    """
    patrimonio_id = request.form.get('patrimonio_id')
    novo_valor = request.form.get('novo_valor')

    if not patrimonio_id or not novo_valor:
        # Dados insuficientes para atualização
        flash('Dados insuficientes para atualização', 'error')
        return redirect(url_for('user.visualizar_patrimonio'))

    patrimonio = Patrimonios.query.get(patrimonio_id)
    if patrimonio:
        # Atualiza o patrimônio
        patrimonio.denominacao_de_imobiliario = novo_valor
        db.session.commit()
        # Patrimônio atualizado 
        return redirect(url_for('user.visualizar_patrimonio'))
    else:
        # Patrimônio não encontrado
        return redirect(url_for('user.visualizar_patrimonio'))



@bp_user.route("/criar", methods =["POST"])
@login_required
def criar_patrimonio():
    pass

#teste de funcionalidade de camera
@bp_user.route("/camera")
def mostrar_camera():
    return render_template("./sistema/camera.html")