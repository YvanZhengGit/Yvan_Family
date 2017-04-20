from flask import Blueprint

testhome = Blueprint('testhome', __name__, url_prefix='/testhome')

import forms, views