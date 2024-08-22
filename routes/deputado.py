from flask import Blueprint, render_template

deputado_route = Blueprint('deputado', __name__)

@deputado_route.route('/')
def home():
    return render_template('qualquer.html')