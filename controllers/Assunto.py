from flask import Flask, render_template, request, flash, redirect, url_for, make_response, session, Blueprint
from models.Assunto import Assunto
from utils import db

assunto_bp = Blueprint('assunto', __name__, template_folder='templates')