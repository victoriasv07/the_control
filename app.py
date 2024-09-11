from flask import Flask
from flask_login import LoginManager
from config.config import Config
from models.model import db

# Define login_manager fora da função create_app
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.secret_key = "Abacaxi"
    
    app.config.from_object(Config)
    
    # Inicializar as extensões
    db.init_app(app)
    login_manager.init_app(app)
    
    # Importação das blueprints 
    from user import bp_user
    from admin import bp_admin
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
    app = create_app()
    app.run(host='0.0.0.0', debug=True)
