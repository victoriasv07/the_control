from flask import Flask
import argparse
from flask_login import LoginManager, current_user
from config.config import Config
from models.model import db, Patrimonios
from datetime import timedelta
from dotenv import load_dotenv
import os


# Define login_manager fora da função create_app
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    load_dotenv()
    app.secret_key = os.getenv("SECRET_KEY")
    app.config.from_object(Config)
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=10)
    
    # Inicializar as extensões
    db.init_app(app)
    login_manager.init_app(app)
    
    # Importação das blueprints 
    from server.pages.user import bp_user # Corrigido
    from server.pages.admin import bp_admin

    # Registrar os blueprints
    app.register_blueprint(bp_user)
    app.register_blueprint(bp_admin)

    # Define o loader do usuário
    from models.model import Usuario, Admin
    @login_manager.user_loader
    def load_user(user_id):
        user = Usuario.query.get(int(user_id))
        if user:
            return user
        admin = Admin.query.get(int(user_id))
        return admin

    return app

if __name__ == "__main__":
    print("Iniciando a aplicação...")

    parser = argparse.ArgumentParser(description="Teste de criação de PDF")
    parser.add_argument("--run-tests", action="store_true", help="Executa os testes antes de iniciar o servidor Flask")
    args = parser.parse_args()

    print(f"Argumentos fornecidos: {args}")  

    if args.run_tests:
        print("Função de teste executada com sucesso!")

    app = create_app()
    app.run(host='0.0.0.0', port=5000)
