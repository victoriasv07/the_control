from flask_sqlalchemy import SQLAlchemy
import os
class Config():
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI", "mysql+pymysql://root:5e5i_123@localhost/the_control")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
