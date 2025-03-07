from flask import Flask, render_template, request, flash, redirect, url_for, make_response, session, Blueprint
from models.Progresso import Progresso
from utils import db

progresso_bp = Blueprint('progresso', __name__, template_folder='templates')