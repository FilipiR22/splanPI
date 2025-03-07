from flask import Flask, render_template, request, flash, redirect, url_for, make_response, session, Blueprint
from models.Conteudo import Conteudo
from utils import db

conteudo_bp = Blueprint('conteudo', __name__, template_folder='templates')