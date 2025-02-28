from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, flash, redirect, url_for, make_response, session, Blueprint
import sqlite3
from flask_login import LoginManager
import re

db = SQLAlchemy()
login_manager = LoginManager()
# banco = sqlite3.connect('splan.db')

def validar_telefone(telefone):
    if re.match(r'^\(?\d{2}\)?[\s-]?\d{4,5}[-]?\d{4}$', telefone):
        return True
    return False
    

def validar_email(email):
    if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        return True
    return False