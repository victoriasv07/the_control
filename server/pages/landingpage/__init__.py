from flask import Blueprint

bp_site = Blueprint('site', __name__, url_prefix='/')

from .route import *