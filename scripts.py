<<<<<<< HEAD
#Criar cronograma
#pegar horas totais de estudo do user
#somar os pesos das materias
#dividir o tempo total pela soma dos pesos
#distribuir essa unidade de tempo para cada materia(multiplicar essa unidade de tempo pelo peso da materia para obter o tempo total)
=======
from flask import Flask, render_template, request, flash, redirect, url_for, make_response, session, Blueprint
from models.Formulario import Formulario
from models.Materia import Materia
from models.Materia_peso import Materia_peso
from utils import db, login_manager
from flask_login import current_user
from flask_login import login_user, logout_user, login_required
>>>>>>> dev


