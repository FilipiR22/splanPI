from flask import Flask, render_template, request, flash, redirect, url_for, make_response, session, Blueprint
from models.Formulario import Formulario
from models.Materia import Materia
from models.Materia_peso import Materia_peso
from models.Progresso import Progresso
from models.Assunto import Assunto
from utils import db, login_manager
from flask_login import current_user
from flask_login import login_user, logout_user, login_required

formulario_bp = Blueprint('formulario', __name__, template_folder='templates')


@formulario_bp.route('/responder')
def carregar_formulario():
   return render_template('formulario.html')


@formulario_bp.route('/receberformulario', methods=['POST'])
def processar_formulario():
   # if request.method == "GET":
   #    return render_template('formulario.html')
    
#cadastrar formulario
   horas_estudo = request.form['horas_estudo']
   form = Formulario(current_user.id, horas_estudo)
   print(current_user.id, horas_estudo)
   db.session.add(form)
   db.session.commit()

   id_form = form.id_formulario

#cadastrar pesos e materias
   materias_selecionadas = request.form.getlist("materias[]")

   lista_materias = ['matematica', 'portugues', 'fisica', 'quimica', 'biologia', 'geografia', 'historia', 'literatura', 'artes', 'filosofia', 'sociologia', 'ingles']
   
   dificuldades = {}
   soma_pesos = 0
   

   for materia in lista_materias:
      if materia in materias_selecionadas:
         dificuldade = request.form['dificuldade_'+materia]
         soma_pesos += int(dificuldade)
         dificuldades[materia] = dificuldade
         pegar_materia = Materia.query.filter_by(nome=materia).first()
         id_mat = pegar_materia.id_materia
         print(dificuldade, id_form, id_mat)
         instancia = Materia_peso(dificuldade, id_form, id_mat)
         db.session.add(instancia)
         db.session.commit()

   
   unidade_tempo = int(horas_estudo) / soma_pesos

   tempos_materias = {materia: float(dificuldade) * unidade_tempo for materia, dificuldade in dificuldades.items()}
   
   print(dificuldades)
   print(unidade_tempo)
   print(tempos_materias)
   print(materias_selecionadas)
   print(soma_pesos)
   print(dificuldades.keys())
   print(dificuldades.values())
  

   return redirect(url_for('inicio'))



def dados_cronograma():
   formulario = Formulario.query.filter_by(id_usuario=current_user.id).first()
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

@formulario_bp.route('cronograma')
def criar_cronograma():
   materias_pesos = dados_cronograma()
   ids_tempos = {}

   for mat, tempo in materias_pesos.items():
      obj_mat = Materia.query.filter_by(nome=mat).first()
      ids_tempos[obj_mat.id_materia] = tempo

   print(ids_tempos)
   lista_assuntos = []

   for mat, tempo in ids_tempos.items():
      assuntos = Assunto.query.filter_by(id_materia=mat).all()
      for ass in assuntos:
         progresso = Progresso.query.filter(Progresso.id_assunto==ass.id_assunto, Progresso.id_usuario==current_user.id).first()
         if progresso:
            if progresso.concluido == True:
               print('assunto ja estudado')
               #assunto ja estudado
               continue
            #assunto nao iniciado mas nao concluido
            if (ass.duracao - progresso.tempo_estudado) > tempo:
               print('assunto nao concluido ainda')
               progresso.tempo_estudado += tempo
               db.session.add(progresso)
               db.session.commit()
               break
            elif (ass.duracao - progresso.tempo_estudado) == tempo:
               progresso.concluido = 1
               progresso.tempo_estudado = ass.duracao
               db.session.add(progresso)
               db.session.commit()
               break
            elif (ass.duracao - progresso.tempo_estudado) < tempo:
               progresso.concluido = 1
               progresso.tempo_estudado = ass.duracao
               tempo -= (ass.duracao - progresso.tempo_estudado)
               db.session.add(progresso)
               db.session.commit()
               continue
               #proximo assunto e assim por diante
         #assunto nao iniciado
         if tempo > ass.duracao:
            print('assunto nao iniciado ainda')
            #criar progresso ja concluido - apenas registrar o progresso
            pgs = Progresso(1, ass.duracao, current_user.id, ass.id_assunto)
            print(1, ass.duracao, current_user.id, ass.id_assunto)
            #pegar tempo restante e jogar em outro assunto
            tempo -= ass.duracao
            db.session.add(pgs)
            db.session.commit()
            print('assunto inicado e terminado - tempo de sobra')
            continue
            #criar um laço para que faça ate o tempo acabar e sem precisar fazer 10000000 de if
         elif tempo == ass.duracao:
            print('assunto inicado e terminado - tempo exato')
            pgs = Progresso(1, ass.duracao, current_user.id, ass.id_assunto)
            db.session.add(pgs)
            db.session.commit()
            break
            print(1, ass.duracao, current_user.id, ass.id_assunto)
         elif tempo < ass.duracao:
            print('assunto nao iniciado')
            pgs = Progresso(0, tempo, current_user.id, ass.id_assunto)
            print(0, tempo, current_user.id, ass.id_assunto)
            db.session.add(pgs)
            db.session.commit()
            print('assunto inicado mas nao terminado - tempo curto')
            break
 

   return render_template('teste.html', materias_pesos=materias_pesos)
