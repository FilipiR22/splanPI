from flask import Flask, render_template, request, flash, redirect, url_for, make_response, session, Blueprint
from models.Progresso import Progresso
from utils import db

progresso_bp = Blueprint('progresso', __name__, template_folder='templates')

@progresso_bp.route('/', methods=['POST'])
def criar_progresso():
    concluido = request.form['concluido']
    id_usuario = request.form['id_user']
    id_assunto = request.form['id_assunto']
    tempo_estudado = request.form['tempo_estudado']

    progresso = Progresso(concluido, tempo_estudado, id_usuario, id_assunto)
    db.session.add(progresso)
    db.session.commit()

    return render_template()


@progresso_bp.route('/atualizarprogresso<int:id_progresso>')
def update_progresso(id_progresso):
    progresso = Progresso.query(id_progresso)

    progresso.concluido = request.form['concluido']
    progresso.tempo_estudado = request.form['tempo_estudado']

    db.session.add(progresso)
    db.session.commit()

    return redirect(url_for('.recuperaaprogresso', id_progresso=id_progresso))


@progresso_bp.route('/recuperarprogresso<int:id_progresso>')
def recuperar_progresso(id_progresso):
    progresso = Progresso.query(id_progresso)
    db.session.commit()

    return progresso


@progresso_bp.route('/deletarprogresso<int:id_progresso>')
def deletar_progresso(id_progresso):
    progresso = Progresso.query(id_progresso)
    db.session.delete(progresso)
    db.session.commit()

    return redirect()