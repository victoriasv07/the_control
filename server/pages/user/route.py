from flask import Blueprint, jsonify, request, render_template, redirect, url_for, flash, session, send_file
from flask_login import login_required, logout_user, login_user, current_user
from models.model import db, Patrimonios, Cadastro, Usuario, Admin
from utils.pdf_generator import criar_pdf


bp_user = Blueprint("user", __name__)



@bp_user.route("/home")
@login_required
def home():
    return render_template("./sistema/user/home.html")

##rota base sistemas
@bp_user.route("/sistema")
@login_required
def sistema():
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
    return redirect(url_for('user.login'))



##rota de login usuario
@bp_user.route("/login", methods=["POST", "GET"])
def login():
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
            return redirect(url_for("user.home"))
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
def register():
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
        return redirect(url_for("user.login"))

    # Se o método for GET, retorna o formulário de cadastro
    return render_template("./sistema/cadastro.html")

#rota para filtrar salas a partir da navbar


@bp_user.route("/filtrar", methods=["POST", "GET"])
@login_required
def visualizar_patrimonio(): 
    """
    Rota para visualizar e deletar patrimônios por sala ou realizar uma pesquisa com base em um termo fornecido.
    """
    # Obtém o valor da query e o valor da sala a partir dos parâmetros GET
    query = request.args.get("query")
    sala = request.args.get("sala")

    # Obter as salas distintas para popular o dropdown
    distinct_locals = db.session.query(Patrimonios.local).distinct().all()
    salas = [local[0] for local in distinct_locals]  # Extrair os valores em uma lista

    # Realiza a exclusão do patrimônio se o método for POST
    if request.method == "POST":
        patrimonio_id = request.form.get("patrimonio_id")
        if patrimonio_id:
            patrimonio = Patrimonios.query.get(patrimonio_id)
            if patrimonio:
                db.session.delete(patrimonio)
                db.session.commit()
                flash(f"Patrimônio ID {patrimonio_id} excluído com sucesso!", "success")
    
    # Inicia a consulta de patrimônio sem filtros
    patrimonios = Patrimonios.query

    # Filtra os patrimônios pelo parâmetro sala, se fornecido
    if sala:
        try:
            sala_inteiro = int(sala)  # Tenta converter o valor para inteiro
            patrimonios = patrimonios.filter_by(local=sala_inteiro)
        except ValueError:
            patrimonios = patrimonios.filter_by(local=sala)

    if query:
        #filtra o banco a partir da query passada
        patrimonios = patrimonios.filter(
            (Patrimonios.denominacao_de_imobiliario.ilike(f'%{query}%')) |
            (Patrimonios.numero_de_etiqueta.ilike(f'%{query}%')) |
            (Patrimonios.local.ilike(f'%{query}%'))
        )
        
    #exibe toda a pesquisa filtrada
    patrimonios = patrimonios.all()
    return render_template("./sistema/user/layout.html", patrimonios=patrimonios, sala=sala, salas=salas, query=query)

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
    sala = request.form.get('sala')
    if not patrimonio_id:
        return 'ID do patrimônio não fornecido', 400
    
    patrimonio = Patrimonios.query.get(patrimonio_id)
    if patrimonio:
        db.session.delete(patrimonio)
        db.session.commit()
        ##Patrimônio deletado 
        return redirect(url_for('user.visualizar_patrimonio', sala = sala))
    else:
        return redirect(url_for('user.visualizar_patrimonio', sala = sala))



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
    if request.method =="POST":
        numero_de_etiqueta = request.form.get("cadastrar_numero_de_etiqueta")
        nome = request.form.get("cadastrar_nome")
        data_de_chegada = request.form.get("cadastrar_data_de_chegada")
        local = request.form.get("cadastrar_local")
        
        novo_patrimonio = Patrimonios(numero_de_etiqueta = numero_de_etiqueta, denominacao_de_imobiliario =nome, data_de_chegada = data_de_chegada, local = local)
        db.session.add(novo_patrimonio)
        db.session.commit()
        return redirect(url_for("user.home"))
    
@bp_user.route("/exportar", methods=["GET", "POST"])
@login_required
def exportar():
    """
    Essa rota exporta a tabela de patrimônios para um arquivo PDF.

    Ela recebe o parâmetro "sala" via GET e o usa para filtrar os patrimônios.
    Se o parâmetro "sala" for fornecido, ele exporta os patrimônios dessa sala.
    Caso contrário, ele retorna todos os patrimônios.

    A rota chama a função criar_pdf() para gerar o arquivo PDF.
    """
    args = request.args.get("sala")
    pdf_filename = criar_pdf(args)
    # Retorna o arquivo PDF para download
    return send_file(pdf_filename, as_attachment=True)


#teste de funcionalidade de camera
@bp_user.route("/camera")
def mostrar_camera():
    return render_template("./sistema/camera.html")
