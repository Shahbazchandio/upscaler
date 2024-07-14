from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.models.ai_model import AIModel
from app import db

bp = Blueprint('dashboard', __name__)

@bp.route('/')
@login_required
def index():
    return render_template('dashboard.html')

@bp.route('/models', methods=['GET', 'POST'])
@login_required
def manage_models():
    if request.method == 'POST':
        name = request.form['name']
        model_type = request.form['type']
        file_path = request.form['file_path']
        new_model = AIModel(name=name, type=model_type, file_path=file_path)
        db.session.add(new_model)
        db.session.commit()
        flash('New model added successfully')
        return redirect(url_for('dashboard.manage_models'))
    
    models = AIModel.query.all()
    return render_template('model_management.html', models=models)

@bp.route('/models/<int:id>/toggle', methods=['POST'])
@login_required
def toggle_model(id):
    model = AIModel.query.get_or_404(id)
    model.is_active = not model.is_active
    db.session.commit()
    return redirect(url_for('dashboard.manage_models'))