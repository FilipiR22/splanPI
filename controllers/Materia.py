from flask import Flask, render_template, request, flash, redirect, url_for, make_response, session, Blueprint
from models.Materia import Materia
from utils import db
from models.Assunto import Assunto
from flask_login import current_user

materia_bp = Blueprint('materia', __name__, template_folder='templates')

@materia_bp.route('/<materia>')
def listar_assuntos(materia):
    mat = Materia.query.filter_by(nome=materia).first()
    lista_objs_assuntos = Assunto.query.filter_by(id_materia=mat.id_materia).all() 
    if current_user.tipo_user == 'adm':
        return render_template('carregar_materias_adm.html', assuntos=lista_objs_assuntos, materia=mat)
    return render_template('carregarmaterias.html', assuntos=lista_objs_assuntos, materia=mat)