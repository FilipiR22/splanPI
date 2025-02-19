from flask import Flask, render_template, request, flash, redirect, url_for, make_response, session, Blueprint
from models.Assunto import Assunto
from utils import db

assunto_bp = Blueprint('assunto', __name__, template_folder='templates')


@assunto_bp.route('/recuperarassunto/<int:id_assunto>')
def recuperar_assunto(id_assunto):
    assunto = Assunto.query(id_assunto)
    db.session.commit()

    return render_template()

@assunto_bp.route('/assuntos')
def carregar_assuntos():
    assuntos = Assunto.query.all()
    db.session.commit()

    #filtra por id da materia com uma consulta join

    return assuntos


@assunto_bp.route('/updateassunto<int:id_assunto>', methods=['POST'])
def carregar_assunto(id_assunto):
    assunto = Assunto.query(id_assunto)

    assunto.duracao = request.form['duracao']

    db.session.add(assunto)
    db.session.commit()

    return redirect(url_for('.recuperarassunto', id_assunto=id_assunto))


@assunto_bp.route('/deletarassunto<int:id_assunto>')
def deletar_assunto(id_assunto):
    db.session.delete(Assunto).filter(id_assunto=id_assunto)
    db.session.commit()

    return redirect(url_for('.recuperarassunto', id_assunto=id_assunto))