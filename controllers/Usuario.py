from flask import Flask, render_template, request, flash, redirect, url_for, make_response, session, Blueprint
from models.Usuario import Usuario
from utils import db, login_manager, validar_email, validar_telefone
import hashlib
from flask_login import current_user
from flask_login import login_user, logout_user, login_required
import re
from models.Formulario import Formulario
from models.Progresso import Progresso
from models.Materia_peso import Materia_peso

user_bp = Blueprint('usuario', __name__, template_folder='templates')


@login_manager.user_loader
def load_user(user_id):
    # print(f"Tentando carregar usuário com ID: {user_id}")
    if not user_id:
        return None  
    return Usuario.query.get(user_id)



@user_bp.route('/cadastro', methods=['POST', 'GET'])
def criar_usuario():
    if request.method == 'GET':
        return render_template('signup.html')
 
    nome = request.form['nome']
    telefone = request.form['telefone']
    senha = request.form['senha']
    confirmarsenha = request.form['confirmarsenha']
    tipo_user = request.form['tipo_user']
    email = request.form['email']

    if validar_email(email) != True:
        flash('Email inválido!', 'warning')
        return redirect(url_for('usuario.criar_usuario'))
    
    if validar_telefone(telefone) != True:
        flash('Telefone inválido!', 'warning')
        return redirect(url_for('usuario.criar_usuario'))

    user_existente = Usuario.query.filter_by(email=email).first()
    if user_existente:
        flash('Email já cadastrado. Faça login!', 'warning')
        return render_template('login.html')
    elif senha != confirmarsenha:
        flash('Senha e confirmação de senha precisam ser iguais!', 'warning')
        return redirect(url_for('usuario.criar_usuario'))
    
    hash_senha = hashlib.sha256(senha.encode()).hexdigest()
    user = Usuario(nome, telefone, email, hash_senha, tipo_user)
    db.session.add(user)
    db.session.commit()
    login_user(user)
    
    if current_user.tipo_user == 'adm':
        return redirect(url_for('dashboard_adm'))
    return redirect(url_for('formulario.carregar_formulario'))
    


@user_bp.route('/login', methods=['POST', 'GET'])
def login_usuario():
    if request.method == 'GET':
        if current_user.is_authenticated:
            if current_user.tipo_user == 'adm':
                return redirect(url_for('dashboard_adm'))
            return redirect(url_for('inicio'))
        return render_template('login.html')
    
    email = request.form['email']
    senha = request.form['senha']

    user = Usuario.query.filter_by(email=email).first()

    if user:
        hash_senha = hashlib.sha256(senha.encode()).hexdigest()
        if user.senha == hash_senha:
            login_user(user)
            # print(f'Usuário logado: {user.id}')
            if current_user.tipo_user == 'adm':
                return render_template('onboarding_adm.html')
            return redirect(url_for('inicio'))
        else:
            flash('Senha incorreta!', 'warning')
            return redirect(url_for('usuario.login_usuario'))
    else:
        flash('Email inválido!', 'warning')
        return redirect(url_for('usuario.login_usuario'))
    


#fazer funcionalidade de exigir login para poder fazer update
@user_bp.route('/alterarperfil', methods=['POST'])
@login_required
def update_user():
    if request.method == 'GET':
        return redirect(url_for('usuario.carregar_perfil'))
    user = current_user
    
    senha = hashlib.sha256(request.form['novasenha'].encode()).hexdigest()
    confirmacaosenha = hashlib.sha256(request.form['confirmacaonovasenha'].encode()).hexdigest()
    if request.form['nome'] == user.nome and request.form['email'] == user.email and request.form['telefone'] == user.telefone and senha == user.senha and senha == confirmacaosenha:
        flash('Nenhuma informação foi atualizada!', 'warning')
        return redirect(url_for('usuario.carregar_perfil'))

    if request.form['nome'] != user.nome:
        user.nome = request.form['nome']

    if request.form['email'] != user.email:
        if validar_email(request.form['email']) != True:
            flash('Email inválido!', 'warning')
            return redirect(url_for('usuario.carregar_perfil'))
        user.email = request.form['email']

    if request.form['telefone'] != user.telefone:
        if validar_telefone(request.form['telefone']) != True:
            flash('Telefone inválido!', 'warning')
            return redirect(url_for('usuario.carregar_perfil'))
        user.telefone = request.form['telefone']

    
    if senha != user.senha:
        if senha == confirmacaosenha:
            user.senha = senha
        flash('Senha e confirmação não são iguais', 'warning')
        return redirect(url_for('usuario.carregar_perfil'))
            

    db.session.add(user)
    db.session.commit()
    
    return redirect(url_for('inicio'))


@user_bp.route('/deletarperfil')
@login_required
def deletar_user():
    if not current_user.is_authenticated:
        return redirect(url_for("login")) 
    
    #deletar formulario e materia_peso
    form = Formulario.query.filter_by(id_usuario=current_user.id).first()
    lista_materia_peso = Materia_peso.query.filter_by(id_formulario=form.id_formulario).all()
    for obj in lista_materia_peso:
        db.session.delete(obj)
        db.session.commit()

    db.session.delete(form)
    db.session.commit()

    lista_progressos = Progresso.query.filter_by(id_usuario=current_user.id)
    for obj in lista_progressos:
        db.session.delete(obj)
        db.session.commit()

    user = Usuario.query.get(current_user.id)
    logout_user()
    db.session.delete(user)
    db.session.commit()
    session.pop('user', None)
    
    return redirect(url_for('index'))


@user_bp.route('/admdeletaruser/<int:id>')
@login_required
def adm_deletar_user(id):
    if not current_user.is_authenticated:
        return redirect(url_for("login")) 
    
    #deletar formulario e materia_peso
    form = Formulario.query.filter_by(id_usuario=id).first()
    lista_materia_peso = Materia_peso.query.filter_by(id_formulario=form.id_formulario).all()
    for obj in lista_materia_peso:
        db.session.delete(obj)
        db.session.commit()

    db.session.delete(form)
    db.session.commit()

    lista_progressos = Progresso.query.filter_by(id_usuario=id)
    for obj in lista_progressos:
        db.session.delete(obj)
        db.session.commit()

    user = Usuario.query.get(id)
    db.session.delete(user)
    db.session.commit()
    session.pop('user', None)
    
    return redirect(url_for('gerenciar_users'))



@user_bp.route('/logoff')
@login_required
def logoff():
    if not current_user.is_authenticated:
        return redirect(url_for("login")) 
    logout_user() 
    session.clear()
    return redirect(url_for('index'))


@user_bp.route('/perfil')
@login_required
def carregar_perfil():
    if current_user.tipo_user == 'adm':
        return render_template('perfil_adm.html', user=current_user)
    return render_template('perfil_user.html', user=current_user)

