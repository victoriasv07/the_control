from flask import Blueprint, jsonify, request, render_template
from models.model import db, Patrimonios
bp_site = Blueprint("site", __name__)

@bp_site.route("/")
def index():
    return render_template("./site/index.html")