from flask import Blueprint, jsonify, request, render_template, redirect, url_for, flash, session, send_file
from flask_login import login_required, logout_user, login_user, current_user
from models.model import db, Patrimonios, Cadastro, Usuario, Admin, Rastreio_patrimonio
from utils.pdf_generator import criar_pdf
from utils.csv_generator import criar_csv
import datetime
import time

bp_user = Blueprint("user", __name__)

@bp_user.route("/home")
@login_required
def home():
    infos_usuarios = Cadastro.query.all()
    movimentacao_de_ativos = Rastreio_patrimonio.query.all()
    print(f"Requisições de usuários encontradas: {infos_usuarios}")
    print(f"Movimentação de ativos encontradas: {movimentacao_de_ativos}")    
    return render_template("./sistema/user/home.html", infos_usuarios=infos_usuarios, movimentacao_de_ativos = movimentacao_de_ativos)


@bp_user.route("/autorizar_usuario/<int:id>", methods=["POST"])
@login_required
def autorizar_usuario(id):
    # Verifica se o usuário logado é Admin
    if current_user.__class__.__name__ != 'Admin':
        return redirect(url_for('user.home'))  # Redireciona se não for admin
    
    usuario_a_autorizar = Cadastro.query.get(id)

    if not usuario_a_autorizar:
        print("Usuário não encontrado.")
        return redirect(url_for('user.home'))
    ##cria um novo registro na Tabela Usuario
    novo_usuario = Usuario(
        nome=usuario_a_autorizar.nome,
        cpf=usuario_a_autorizar.cpf,
        email=usuario_a_autorizar.email,
        telefone=usuario_a_autorizar.telefone,
        password=usuario_a_autorizar.password
    )

    db.session.add(novo_usuario)
    db.session.delete(usuario_a_autorizar)
    db.session.commit()

    flash(f"Usuário {novo_usuario.nome} autorizado com sucesso!", "success")
    return redirect(url_for('user.home'))


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
    if request.method == "POST":
        cpf = request.form.get("cpf")
        email = request.form.get("email")
        password = request.form.get("password")

        # Validação do CPF
        if len(cpf) != 11:
            flash("O CPF deve ter exatamente 11 dígitos.", "error")
            return redirect(url_for("user.login")) 

        
        # Verificação de usuário comum
        user = Usuario.query.filter_by(cpf=cpf, email=email, password = password).first()
        if user:
            flash("Usuário logado com sucesso!", "success")
            login_user(user)
            return redirect(url_for("user.home"))

        # Verificação de administrador
        admin = Admin.query.filter_by(cpf=cpf, email=email, password = password).first()
        if admin:
            flash("Administrador logado com sucesso!", "success")
            login_user(admin)
            return redirect(url_for("user.home"))
        
        user_not_admissed = Cadastro.query.filter_by(cpf = cpf, email = email, password = password)
        if user_not_admissed:
            flash("Usuário ainda não admitido, espere seu email", "error")
            return redirect(url_for("user.login"))
        # Caso nenhum usuário ou admin seja encontrado
        flash("Email ou CPF inválido.", "error")
        return redirect(url_for("user.login"))  # Redireciona para o login novamente

    return render_template("./sistema/login.html")


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
        password = request.form.get('password')
        
        # Criar um novo usuário
        novo_usuario = Cadastro(nome=nome, cpf=cpf, telefone=telefone, email=email,password=password)

        # Adicionar o novo usuário ao banco de dados
        db.session.add(novo_usuario)
        db.session.commit()
        flash("Sua conta foi registrada, espere o admin autoriza-lo(a)", "success")
        # Redirecionar para a página de login
        return redirect(url_for("user.login"))

    # Se o método for GET, retorna o formulário de cadastro
    return render_template("./sistema/cadastro.html")

#rota para filtrar salas a partir da navbar

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
        flash("Sucesso ao criar patrimônio", "success")
        return redirect(url_for("user.home"))

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
    Se o p'atrimônio não for encontrado, ele retorna um erro 404.
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
        flash('Patrimônio deletado com sucesso', 'success')
        return redirect(url_for('user.visualizar_patrimonio', sala = sala))
    else:
        flash('Patrimônio Não encontrado', 'error')
        return redirect(url_for('user.visualizar_patrimonio', sala = sala))



mudancas_patrimonio = {}

# Rota para atualizar patrimônio
@bp_user.route("/atualizar", methods=["POST"])
@login_required
def atualizar_patrimonio():
    patrimonio_id = request.form.get('editar_id')
    numero_de_etiqueta = request.form.get('editar_numero_de_etiqueta')
    nome = request.form.get('editar_nome')
    data_de_chegada = request.form.get('editar_data_de_chegada')
    local_novo = request.form.get('editar_local')

    if not patrimonio_id:
        print("Erro: ID do patrimônio não foi enviado.")
        return redirect(url_for('user.visualizar_patrimonio'))

    patrimonio = Patrimonios.query.get(patrimonio_id)
    if patrimonio:
        # Verifica se o local foi alterado
        if patrimonio.local != local_novo:
            local_antigo = patrimonio.local  # Armazena o local antigo
            mudancas_patrimonio[patrimonio_id] = {
                'numero_de_etiqueta': patrimonio.numero_de_etiqueta,
                'nome': patrimonio.denominacao_de_imobiliario,
                'data_de_chegada': patrimonio.data_de_chegada,
                'local_antigo': local_antigo,
                'local_novo': local_novo,
                'data_mudanca': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # Cria um novo registro de rastreio na tabela 'Rastreio_patrimonio'
            rastreio = Rastreio_patrimonio(
                nome=nome,  
                patrimonio_id=patrimonio_id, 
                local_antigo=local_antigo,  
                local_novo=local_novo, 
                data_mudanca=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Data da mudança
            )
            db.session.add(rastreio)  # Adiciona o novo rastreio na sessão

        # Atualiza o patrimônio
        patrimonio.numero_de_etiqueta = numero_de_etiqueta
        patrimonio.denominacao_de_imobiliario = nome
        patrimonio.data_de_chegada = data_de_chegada
        patrimonio.local = local_novo  # Atualiza com o novo local
        db.session.commit()  # Salva as mudanças no banco de dados

        flash(f'Patrimônio {patrimonio_id} atualizado com sucesso', 'success')
        print(mudancas_patrimonio)
    else:
        flash(f'Patrimônio {patrimonio_id} não encontrado', 'error')
        return redirect(url_for('user.visualizar_patrimonio'))

    return redirect(url_for('user.visualizar_patrimonio'))

    
@bp_user.route("/exportar/pdf", methods=["GET", "POST"])
@login_required
def exportar_pdf():
    """
    Essa rota exporta a tabela de patrimônios para um arquivo PDF.

    Ela recebe o parâmetro "sala" via GET e o usa para filtrar os patrimônios.
    Se o parâmetro "sala" for fornecido, ele exporta os patrimônios dessa sala.
    Caso contrário, ele retorna todos os patrimônios.

    A rota chama a função criar_pdf() para gerar o arquivo PDF.
    """
    args = request.args.get("sala")
    pdf_filename = criar_pdf(args)
    flash("Sucesso ao exportar pdf", "success")
    # Retorna o arquivo PDF para download
    return send_file(pdf_filename, as_attachment=True)


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

@bp_user.route("/exportar/csv", methods=["GET", "POST"])
@login_required
def exportar_csv():
    args = request.args.get("sala")
    csv_filename = criar_csv(args)
    flash("Sucesso ao exportar csv", "success")
    return send_file(csv_filename, as_attachment=True)


#teste de funcionalidade de camera
@bp_user.route("/camera")
@login_required
def mostrar_camera():
    return render_template("./sistema/camera.html")

@bp_user.route("/lerbarcode", methods=["POST"])
@login_required
def ler_barcode():
    #terminar de desenvolver funcionalidade de aidção de patrimônio a partir da camêra
    data = request.get_json()
    if not data or 'codigo' not in data:
        return jsonify({"erro": "Código de barras não encontrado"}), 400

    codigo_barras = data['codigo']
    print(f"Código de barras recebido: {codigo_barras}")
    return jsonify({"mensagem": "Código de barras processado com sucesso", "codigo": codigo_barras}), 200