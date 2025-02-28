from flask import Flask, render_template, request, flash, redirect, make_response, session, url_for
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, declarative_base
import json
import os
from flask_migrate import Migrate
from utils import db, login_manager
from controllers.Usuario import user_bp
from controllers.Materia import materia_bp
from controllers.Assunto import assunto_bp
from controllers.Conteudo import conteudo_bp
from controllers.Formulario import formulario_bp, mostrar_assuntos, atualizar_cronogramas
from controllers.Progresso import progresso_bp
from controllers.Materia_peso import peso_bp
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from models.Assunto import Assunto
from models.Conteudo import Conteudo
from models.Materia import Materia
from models.Usuario import Usuario
from models.Progresso import Progresso

app = Flask(__name__)

app.register_blueprint(user_bp, url_prefix='/usuario')
app.register_blueprint(materia_bp, url_prefix='/materia')
app.register_blueprint(assunto_bp, url_prefix='/assunto')
app.register_blueprint(conteudo_bp, url_prefix='/conteudo')
app.register_blueprint(formulario_bp, url_prefix='/formulario')
app.register_blueprint(progresso_bp, url_prefix='/progresso')
app.register_blueprint(peso_bp, url_prefix='/peso')

app.config['SECRET_KEY'] = 'sua palavra secreta'

# db_usuario = os.getenv('DB_USERNAME')
# db_senha = os.getenv('DB_PASSWORD')
# db_host = os.getenv('DB_HOST')
# db_mydb = os.getenv('DB_DATABASE')
# conexao = f"mysql+pymysql://{db_usuario}:{db_senha}@{db_host}/{db_mydb}"
basedir = os.path.abspath(os.path.dirname(__file__))
conexao = f"sqlite:///{os.path.join(basedir, 'instance', 'banco_splan.sqlite')}"
app.config['SQLALCHEMY_DATABASE_URI'] = conexao
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

#flask login
login_manager.init_app(app)
login_manager.login_view = "usuario.login_usuario"

@login_manager.unauthorized_handler
def unauthorized():
   flash("Por favor, faça login para acessar esta página!", 'warning')
   return redirect(url_for('usuario.login_usuario'))



@app.route('/')
def index():
   return render_template('home.html')


@app.route('/dashboard')
@login_required
def inicio():
   return render_template('onboarding.html')


@app.route('/cronograma')
@login_required
def carregar_cronograma():
   assuntos = mostrar_assuntos()

   materias = []
   for ass in assuntos:
      assunto = Assunto.query.filter_by(nome=ass).first()
      materia = Materia.query.filter_by(id_materia=assunto.id_materia).first()
      materias.append(materia.nome)
   return render_template('cronograma.html', assuntos=assuntos, materias=materias)

   
@app.route('/atualizarcronograma')
@login_required
def resetar_cronograma_semanal():
   atualizar_cronogramas()
   return redirect(url_for('carregar_cronograma'))


@app.route('/dashboardadministrador')
@login_required
def dashboard_adm():
   if current_user.tipo_user != 'adm':
      flash('Acesso exclusivo para administradores!', 'danger')
      return redirect(url_for('inicio'))
   return render_template('base_adm.html')


@app.route('/gerenciarusuarios')
@login_required
def gerenciar_users():
   if current_user.tipo_user != 'adm':
      flash('Acesso exclusivo para administradores!', 'danger')
      return redirect(url_for('inicio'))
   usuarios = Usuario.query.filter_by(tipo_user='comum').all()
   return render_template('gerenciar_usuario.html', usuarios=usuarios)

@app.route('/revisao')
def lista_revisao():
   lista_progressos = Progresso.query.filter_by(id_usuario=current_user.id).all()
   assuntos = []
   for pgs in lista_progressos:
      ass = Assunto.query.filter_by(id_assunto=pgs.id_assunto).first()
      assuntos.append(ass.nome)
   return render_template('revisao.html', assuntos=assuntos)


if __name__ == "__main__":
   app.run(debug=True)

