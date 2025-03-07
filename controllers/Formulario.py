from flask import Flask, render_template, request, flash, redirect, url_for, make_response, session, Blueprint
from models.Formulario import Formulario
from models.Materia import Materia
from models.Materia_peso import Materia_peso
from models.Progresso import Progresso
from models.Assunto import Assunto
from models.Usuario import Usuario
from utils import db, login_manager
from flask_login import current_user
from flask_login import login_user, logout_user, login_required

formulario_bp = Blueprint('formulario', __name__, template_folder='templates')


# @formulario_bp.route('/responder')
# def carregar_formulario():
#    return render_template('formulario.html')


@formulario_bp.route('/receberformulario', methods=['POST'])
@login_required
def inserir_dados_form():
   horas_estudo = request.form['horas_estudo']
   form = Formulario(current_user.id, horas_estudo)
   print(current_user.id, horas_estudo)
   db.session.add(form)
   db.session.commit()
   #formulario inserido
   materias_selecionadas = request.form.getlist("materias[]")
   print("Matérias selecionadas:", materias_selecionadas)
   materias = ['matemática', 'português', 'física', 'química', 'biologia', 'geografia', 'história', 'filosofia', 'sociologia', 'artes', 'inglês', 'literatura']
   for materia in materias:
      if materia in materias_selecionadas:
         peso = request.form['dificuldade_'+materia]
         obj_materia = Materia.query.filter_by(nome=materia).first()
         instancia_materia_peso = Materia_peso(peso, form.id_formulario, obj_materia.id_materia)
         db.session.add(instancia_materia_peso)
         db.session.commit()
   criar_cronograma(current_user)
   return redirect(url_for('inicio'))



def dados_cronograma(usuario):
   formulario = Formulario.query.filter(Formulario.id_usuario==usuario.id).first()
   lista_materias_pesos = Materia_peso.query.filter_by(id_formulario=formulario.id_formulario).all()
   tempo_total = formulario.tempo_total
   
   soma_pesos = 0
   materias_pesos = {}

   for obj in lista_materias_pesos:
      materia = Materia.query.filter_by(id_materia=obj.id_materia).first()
      print(materia)
      materias_pesos[materia.nome]=obj.peso
      print(materias_pesos)
      soma_pesos += obj.peso
      print(soma_pesos)

   unidade_tempo = float(tempo_total) / soma_pesos
   print(unidade_tempo)

   tempos_materias = {materia: float(dificuldade) * unidade_tempo for materia, dificuldade in materias_pesos.items()}
   print(tempos_materias)

   return tempos_materias





def criar_cronograma(usuario):
   materias_pesos = dados_cronograma(usuario)
   ids_tempos = {}

   for mat, tempo in materias_pesos.items():
      obj_mat = Materia.query.filter_by(nome=mat).first()
      ids_tempos[obj_mat.id_materia] = tempo

   print(ids_tempos)
   lista_de_assuntos = []

   for mat, tempo in ids_tempos.items():
      assuntos = Assunto.query.filter_by(id_materia=mat).all()
      for ass in assuntos:
         progresso = Progresso.query.filter(Progresso.id_assunto==ass.id_assunto, Progresso.id_usuario==usuario.id).first()
         if progresso:
            if progresso.concluido == True:
               continue
            if (ass.duracao - progresso.tempo_estudado) > tempo:
               print('assunto nao concluido ainda')
               progresso.tempo_estudado += tempo
               db.session.add(progresso)
               db.session.commit()
               lista_de_assuntos.append(ass.nome)
               print(0, progresso.tempo_estudado, usuario.id, ass.id_assunto)
               break
            elif (ass.duracao - progresso.tempo_estudado) == tempo:
               progresso.concluido = 1
               progresso.tempo_estudado = ass.duracao
               db.session.add(progresso)
               db.session.commit()
               lista_de_assuntos.append(ass.nome)
               break
            elif tempo > (ass.duracao - progresso.tempo_estudado):
               progresso.concluido = 1
               tempo -= (ass.duracao - progresso.tempo_estudado)
               progresso.tempo_estudado = ass.duracao
               db.session.add(progresso)
               db.session.commit()
               lista_de_assuntos.append(ass.nome)
               continue
         if tempo > ass.duracao:
            pgs = Progresso(1, ass.duracao, usuario.id, ass.id_assunto)
            print(1, ass.duracao, usuario.id, ass.id_assunto)
            db.session.add(pgs)
            db.session.commit()
            lista_de_assuntos.append(ass.nome)
            print('assunto inicado e terminado - tempo de sobra')
            tempo -= ass.duracao
            continue
         elif tempo == ass.duracao:
            print('assunto inicado e terminado - tempo exato')
            pgs = Progresso(1, ass.duracao, usuario.id, ass.id_assunto)
            db.session.add(pgs)
            db.session.commit()
            print(1, ass.duracao, usuario.id, ass.id_assunto)
            lista_de_assuntos.append(ass.nome)
            
         elif tempo < ass.duracao:
            print('assunto nao iniciado')
            pgs = Progresso(0, tempo, usuario.id, ass.id_assunto)
            print(0, tempo, usuario.id, ass.id_assunto)
            db.session.add(pgs)
            db.session.commit()
            print('assunto inicado mas nao terminado - tempo curto')
            lista_de_assuntos.append(ass.nome)
            break
   print(lista_de_assuntos) 

   return lista_de_assuntos


def atualizar_cronogramas():
   users = Usuario.query.filter_by(tipo_user='comum').all()
   lista_assuntos = []
   print(users)
   for user in users:
      lista_assuntos.append(criar_cronograma(user))

def mostrar_assuntos():
   assuntos = []
   print(current_user)
   obj_assuntos = Progresso.query.filter(Progresso.concluido==0, Progresso.id_usuario==current_user.id).all()
   print(obj_assuntos)
   for ass in obj_assuntos:
      assunto = Assunto.query.filter_by(id_assunto=ass.id_assunto).first()
      print(assunto.nome)
      assuntos.append(assunto.nome)
   print('assuntos:', assuntos)
   return assuntos

