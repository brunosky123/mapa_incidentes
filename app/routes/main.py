from flask import Blueprint, render_template, session
from app.utils.decorators import login_required

main_bp = Blueprint('main', __name__)

@main_bp.route('/home')
def home():
    return render_template('home.html')

@main_bp.route('/principal')
@login_required # ¡Protegida!
def index():
    current_user = session.get('usuario')
    return render_template('index.html', user=current_user)

@main_bp.route('/segura')
@login_required # ¡Protegida!
def buscarSegura():
    return render_template('ruta_segura.html')

@main_bp.route('/segura2')
@login_required # ¡Protegida!
def buscarSegura2():
    return render_template('ruta_segura2.html') 