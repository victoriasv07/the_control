from flask import Blueprint, jsonify, request, render_template
from models.model import db, Patrimonios
bp_sistema_filho = Blueprint("sistema_filha", __name__)

@bp_sistema_filho.route("/sistemafilho")
def index():
    return render_template("./tablet/sistema_filha.html")