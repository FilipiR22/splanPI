from flask import Flask, render_template, request, flash, redirect, url_for, make_response, session, Blueprint
from models.Materia_peso import Materia_peso
from utils import db

peso_bp = Blueprint('peso', __name__, template_folder='templates')


@peso_bp.route('/')
def criar_peso():
    peso = request.form['peso']
    id_formulario = request.form['id_formulario']
    id_materia = request.form['id_materia']

    peso = Materia_peso(peso, id_formulario, id_materia)

    db.session.add(peso)
    db.session.commit()

    return render_template()


@peso_bp.route('/atualizarpeso/<int:id_materiapeso>')
def atualizar_peso(id_materiapeso):
    peso = Materia_peso.query(id_materiapeso)

    peso.peso = request.form['peso']
    id_formulario = request.form['id_formulario']
    id_materia = request.form['id_materia']

    db.session.add(peso)
    db.session.commit()

    return redirect('/')


@peso_bp.route('/recuperarpeso/<int:id_materiapeso>')
def recuperar_peso(id_materiapeso):
    formulario = Materia_peso.query(id_materiapeso)
    db.session.commit()

    return redirect()


@peso_bp.route('/deletarpeso<int:id_materiapeso>')
def deletar_peso(id_materiapeso):
    db.session.delete(Materia_peso).filter(id_materiapeso=id_materiapeso)
    db.session.commit()

    return redirect()