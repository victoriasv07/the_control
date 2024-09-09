from flask import Flask
from user import bp_user
from admin import bp_admin
from config.config import Config
from models.model import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)    
    app.register_blueprint(bp_user)
    app.register_blueprint(bp_admin)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0', debug=True)
