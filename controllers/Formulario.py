# from flask import Flask, render_template, request, flash, redirect, url_for, make_response, session, Blueprint
# from models.Formulario import Formulario
# from models.Materia import Materia
# from models.Materia_peso import Materia_peso
# from models.Progresso import Progresso
# from models.Assunto import Assunto
# from models.Usuario import Usuario
# from utils import db, login_manager
# from flask_login import current_user
# from flask_login import login_user, logout_user, login_required

# formulario_bp = Blueprint('formulario', __name__, template_folder='templates')


# @formulario_bp.route('/responder')
# @login_required
# def carregar_formulario():
#    return render_template('formulario.html')



# #armazena os dados do formulario no banco
# @formulario_bp.route('/receberformulario', methods=['POST'])
# @login_required
# #pega os dados do formulario e insere na tabela materia peso e formulario
# def inserir_dados_form():
#    horas_estudo = request.form['horas_estudo']
#    form = Formulario(current_user.id, horas_estudo)
#    print(current_user.id, horas_estudo)
#    db.session.add(form)
#    db.session.commit()
#    #formulario inserido

#    materias_selecionadas = request.form.getlist("materias[]")
#    print("Matérias selecionadas:", materias_selecionadas)

#    materias = ['matemática', 'português', 'física', 'química', 'biologia', 'geografia', 'história', 'filosofia', 'sociologia', 'artes', 'inglês', 'literatura']

#    for materia in materias:
#       if materia in materias_selecionadas:
#          peso = request.form['dificuldade_'+materia]
#          obj_materia = Materia.query.filter_by(nome=materia).first()
#          instancia_materia_peso = Materia_peso(peso, form.id_formulario, obj_materia.id_materia)
#          db.session.add(instancia_materia_peso)
#          db.session.commit()

#    criar_cronograma(current_user)
#    return redirect(url_for('inicio'))




# #função que pega as materias e seus respectivos tempos de estudo
# @formulario_bp.route('/dados')
# def dados_cronograma(usuario):
#    formulario = Formulario.query.filter_by(id_usuario=usuario.id).first()
#    lista_materias_pesos = Materia_peso.query.filter_by(id_formulario=formulario.id_formulario).all()
#    tempo_total = formulario.tempo_total
   
#    soma_pesos = 0
#    materias_pesos = {}

#    for obj in lista_materias_pesos:
#       materia = Materia.query.filter_by(id_materia=obj.id_materia).first()
#       print(materia)
#       materias_pesos[materia.nome]=obj.peso
#       print(materias_pesos)
#       soma_pesos += obj.peso
#       print(soma_pesos)

#    unidade_tempo = round((float(tempo_total) / soma_pesos),1)
#    print(unidade_tempo)

#    tempos_materias = {materia: float(dificuldade) * unidade_tempo for materia, dificuldade in materias_pesos.items()}
#    print(tempos_materias)

#    return tempos_materias

   



# #cria/atualiza os progressos
# @formulario_bp.route('/crono')
# def criar_cronograma(usuario):
#    usuario = current_user
#    materias_pesos = dados_cronograma(usuario)
#    ids_tempos = {}

#    for mat, tempo in materias_pesos.items():
#       obj_mat = Materia.query.filter_by(nome=mat).first()
#       ids_tempos[obj_mat.id_materia] = tempo

#    print(ids_tempos)
#    lista_de_assuntos = []

#    for mat, tempo in ids_tempos.items():
#       # assuntos = Assunto.query.filter_by(id_materia=mat).all()
#       assuntos = Assunto.query.filter_by(id_materia=mat).all()
#       for ass in assuntos:
#          progresso = Progresso.query.filter(Progresso.id_assunto==ass.id_assunto, Progresso.id_usuario==usuario.id).first()
#          if progresso:
#             if progresso.concluido == True:
#                # print('assunto ja estudado')
#                #assunto ja estudado
#                continue
#             #assunto nao iniciado mas nao concluido
#             if (ass.duracao - progresso.tempo_estudado) > tempo:
#                print('assunto nao concluido ainda')
#                progresso.tempo_estudado += tempo
#                db.session.add(progresso)
#                db.session.commit()
#                lista_de_assuntos.append(ass.nome)
#                print(0, progresso.tempo_estudado, usuario.id, ass.id_assunto)
#                break
#             elif (ass.duracao - progresso.tempo_estudado) == tempo:
#                progresso.concluido = 1
#                progresso.tempo_estudado = ass.duracao
#                db.session.add(progresso)
#                db.session.commit()
#                lista_de_assuntos.append(ass.nome)
#                break
#             elif tempo > (ass.duracao - progresso.tempo_estudado):
#                progresso.concluido = 1
#                tempo -= (ass.duracao - progresso.tempo_estudado)
#                progresso.tempo_estudado = ass.duracao
#                db.session.add(progresso)
#                db.session.commit()
#                lista_de_assuntos.append(ass.nome)
#                continue
#                #proximo assunto e assim por diante
#          #assunto nao iniciado
#          if tempo > ass.duracao:
#             # print('assunto nao iniciado ainda')
#             #criar progresso ja concluido - apenas registrar o progresso
#             pgs = Progresso(1, ass.duracao, usuario.id, ass.id_assunto)
#             print(1, ass.duracao, usuario.id, ass.id_assunto)
#             #pegar tempo restante e jogar em outro assunto
#             db.session.add(pgs)
#             db.session.commit()
#             lista_de_assuntos.append(ass.nome)
#             print('assunto inicado e terminado - tempo de sobra')
#             tempo -= ass.duracao
#             continue
#             #criar um laço para que faça ate o tempo acabar e sem precisar fazer 10000000 de if
#          elif tempo == ass.duracao:
#             print('assunto inicado e terminado - tempo exato')
#             pgs = Progresso(1, ass.duracao, usuario.id, ass.id_assunto)
#             db.session.add(pgs)
#             db.session.commit()
#             print(1, ass.duracao, usuario.id, ass.id_assunto)
#             lista_de_assuntos.append(ass.nome)
#             #break
            
#          elif tempo < ass.duracao:
#             print('assunto nao iniciado')
#             pgs = Progresso(0, tempo, usuario.id, ass.id_assunto)
#             print(0, tempo, usuario.id, ass.id_assunto)
#             db.session.add(pgs)
#             db.session.commit()
#             print('assunto inicado mas nao terminado - tempo curto')
#             lista_de_assuntos.append(ass.nome)
#             break
#    print(lista_de_assuntos) 
#    print("Lista de Assuntos Criada no Cronograma:", lista_de_assuntos)
#    return lista_de_assuntos




# # def atualizar_cronogramas():
# #    usuarios = Usuario.query.all()

# #    for usuario in usuarios:
# #       criar_cronograma(usuario)





# def mostrar_assuntos():
#    assuntos = []
#    lista_progressos = Progresso.query.filter(Progresso.concluido==0, Progresso.id_usuario==current_user.id).all()

#    print("Debug - Lista de Progressos do Usuário:")
#    for pgs in lista_progressos:
#       print(f"ID Assunto: {pgs.id_assunto}, Tempo Estudado: {pgs.tempo_estudado}, Concluído: {pgs.concluido}")

#    for pgs in lista_progressos:
#       assunto = Assunto.query.filter_by(id_assunto=pgs.id_assunto).first()
#       assuntos.append(assunto.nome)
   
#    print(assuntos)
#    return assuntos



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


@formulario_bp.route('/responder')
def carregar_formulario():
   return render_template('formulario.html')

# #armazena os dados do formulario
# @formulario_bp.route('/receberformulario', methods=['POST'])
# def inserir_dados_form():

# #cadastrar formulario
#    horas_estudo = request.form['horas_estudo']
#    form = Formulario(current_user.id, horas_estudo)
#    print(current_user.id, horas_estudo)
#    db.session.add(form)
#    db.session.commit()

#    id_form = form.id_formulario

# #cadastrar pesos e materias
#    materias_selecionadas = request.form.getlist("materias[]")

#    lista_materias = ['matemática', 'português', 'física', 'química', 'biologia', 'geografia', 'história', 'filosofia', 'sociologia', 'artes', 'inglês', 'literatura']
   
#    dificuldades = {}
#    soma_pesos = 0
   

#    for materia in lista_materias:
#       if materia in materias_selecionadas:
#          dificuldade = request.form['dificuldade_'+materia]
#          soma_pesos += int(dificuldade)
#          dificuldades[materia] = dificuldade
#          pegar_materia = Materia.query.filter_by(nome=materia).first()
#          id_mat = pegar_materia.id_materia
#          print(dificuldade, id_form, id_mat)
#          instancia = Materia_peso(dificuldade, id_form, id_mat)
#          db.session.add(instancia)
#          db.session.commit()

   
#    unidade_tempo = int(horas_estudo) / soma_pesos

#    tempos_materias = {materia: float(dificuldade) * unidade_tempo for materia, dificuldade in dificuldades.items()}
   
#    print(dificuldades)
#    print(unidade_tempo)
#    print(tempos_materias)
#    print(materias_selecionadas)
#    print(soma_pesos)
#    print(dificuldades.keys())
#    print(dificuldades.values())
  

#    return redirect(url_for('inicio'))

@formulario_bp.route('/receberformulario', methods=['POST'])
@login_required
#pega os dados do formulario e insere na tabela materia peso e formulario
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



#função que pega as materias e seus respectivos tempos de estudo
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




#cria/atualiza os progressos
def criar_cronograma(usuario):
   # usuario = current_user
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
               # print('assunto ja estudado')
               #assunto ja estudado
               continue
            #assunto nao iniciado mas nao concluido
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
               #proximo assunto e assim por diante
         #assunto nao iniciado
         if tempo > ass.duracao:
            # print('assunto nao iniciado ainda')
            #criar progresso ja concluido - apenas registrar o progresso
            pgs = Progresso(1, ass.duracao, usuario.id, ass.id_assunto)
            print(1, ass.duracao, usuario.id, ass.id_assunto)
            #pegar tempo restante e jogar em outro assunto
            db.session.add(pgs)
            db.session.commit()
            lista_de_assuntos.append(ass.nome)
            print('assunto inicado e terminado - tempo de sobra')
            tempo -= ass.duracao
            continue
            #criar um laço para que faça ate o tempo acabar e sem precisar fazer 10000000 de if
         elif tempo == ass.duracao:
            print('assunto inicado e terminado - tempo exato')
            pgs = Progresso(1, ass.duracao, usuario.id, ass.id_assunto)
            db.session.add(pgs)
            db.session.commit()
            print(1, ass.duracao, usuario.id, ass.id_assunto)
            lista_de_assuntos.append(ass.nome)
            break
            
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

