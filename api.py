from flask import Blueprint, jsonify, request, render_template
from models.model import db, Patrimonios
bp = Blueprint("api", __name__)

@bp.route("/")
def index():
    return render_template("index.html")