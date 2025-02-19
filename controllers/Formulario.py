from flask import Flask, render_template, request, flash, redirect, url_for, make_response, session, Blueprint
from models.Formulario import Formulario
from utils import db, login_manager
from flask_login import current_user
from flask_login import login_user, logout_user, login_required

formulario_bp = Blueprint('formulario', __name__, template_folder='templates')


@formulario_bp.route('/responder')
def carregar_formulario():
   return render_template('formulario.html')


@formulario_bp.route('/receberformulario', methods=['POST'])
def receber_formulario():
   flash('forms recebido')
   return redirect(url_for('inicio'))