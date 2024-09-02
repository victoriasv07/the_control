from flask import Flask
from api_site import bp_site
from sistema import bp_sistema
from config.config import Config
from models.model import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)    
    app.register_blueprint(bp_site)
    app.register_blueprint(bp_sistema)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0', debug=True)
