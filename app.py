from flask import Flask
from flask_migrate import Migrate
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
    app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=100)
    migrate = Migrate(app=app, db=db)

    # Inicializar as extensões
    db.init_app(app)
    login_manager.init_app(app)

    # Importação das blueprints
    from server.pages.user import bp_user  # Corrigido

    # Registrar os blueprints
    app.register_blueprint(bp_user)

    # Define o loader do usuário
    from models.model import Usuario, Admin

    @login_manager.user_loader
    def load_user(user_id):
        # Verifica primeiro se o usuário logado é um Admin
        admin = Admin.query.get(int(user_id))
        if admin:
            return admin

        # Se não for admin, tenta carregar um usuário comum
        user = Usuario.query.get(int(user_id))
        return user

    return app


if __name__ == "__main__":
    print("Iniciando a aplicação...")
    app = create_app()
    app.run(host="0.0.0.0", port=5000)
