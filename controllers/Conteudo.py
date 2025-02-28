from flask import Flask, render_template, request, flash, redirect, url_for, make_response, session, Blueprint
from models.Conteudo import Conteudo
from utils import db

conteudo_bp = Blueprint('conteudo', __name__, template_folder='templates')


@conteudo_bp.route('/recuperarconteudo/<int:id_conteudo>')
def recuperar_conteudo(id_conteudo):
    conteudo = conteudo.query(id_conteudo)
    db.session.commit()


@conteudo_bp.route('/conteudos')
def carregar_conteudos():
    conteudos = Conteudo.query.all()
    db.session.commit()

    #filtra por id do assunto com uma consulta join

    return conteudos

@conteudo_bp.route('/deletarconteudo<int:id_conteudo>')
def deletar_Conteudo(id_conteudo):
    db.session.delete(Conteudo).filter(id_conteudo=id_conteudo)
    db.session.commit()

    return redirect(url_for('.recuperarconteudo', id_conteudo=id_conteudo))
