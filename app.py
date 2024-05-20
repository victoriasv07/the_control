from flask import Flask
from api import bp
from  config.config import Config
from models.model import db

def create_app():
    app = Flask(__name__)
    app.register_blueprint(bp)
    app.config.from_object(Config)
    db.init_app(app)
    return app




if __name__ == "__main__":
    app = create_app()
    app.run(host = '0.0.0.0', debug=True)