from utils import db

class Formulario(db.Model):
    __tablename__='formulario'
    id_formulario = db.Column(db.Integer, primary_key = True, autoincrement = True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    tempo_total = db.Column(db.Float)

    usuario = db.relationship('Usuario', foreign_keys=id_usuario)


    def __init__(self, id_usuario, tempo_total):
        self.id_usuario = id_usuario 
        self.tempo_total = tempo_total