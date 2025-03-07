from flask import Flask, render_template, request, flash, redirect, url_for, make_response, session, Blueprint
from models.Materia_peso import Materia_peso
from utils import db

peso_bp = Blueprint('peso', __name__, template_folder='templates')