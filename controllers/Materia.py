from flask import Flask, render_template, request, flash, redirect, url_for, make_response, session, Blueprint
from models.Materia import Materia
from utils import db
from models.Assunto import Assunto
from models.Conteudo import Conteudo
from flask_login import current_user

materia_bp = Blueprint('materia', __name__, template_folder='templates')

@materia_bp.route('/<materia>')
def listar_assuntos(materia):
    mat = Materia.query.filter_by(nome=materia).first()
    lista_objs_assuntos = Assunto.query.filter_by(id_materia=mat.id_materia).all() 
    if current_user.tipo_user == 'adm':
        return render_template('carregarmaterias_adm.html', assuntos=lista_objs_assuntos, materia=materia)
    return render_template('carregarmaterias.html', assuntos=lista_objs_assuntos, materia=materia)


@materia_bp.route('/<materia>/<assunto>')
def listar_conteudos(materia, assunto):
    ass = Assunto.query.filter_by(nome=assunto).first()
    print(assunto)
    lista_obj_conteudos = Conteudo.query.filter_by(id_assunto=ass.id_assunto).all()
    if current_user.tipo_user == 'adm':
        return render_template('mostrar_conteudos_adm.html', conteudos=lista_obj_conteudos, assunto=assunto)
    return render_template('mostrar_conteudos.html', conteudos=lista_obj_conteudos, assunto=assunto)