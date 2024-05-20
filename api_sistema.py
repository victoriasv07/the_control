from flask import Blueprint, jsonify, request, render_template
from models.model import db, Patrimonios
bp_sistema = Blueprint("sistema", __name__)

@bp_sistema.route("/sistema")
def index():
    return render_template("./sistema/sistema.html")