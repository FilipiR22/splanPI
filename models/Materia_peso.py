from utils import db

class Materia_peso(db.Model):
    __tablename__='peso'
    id_materia_peso = db.Column(db.Integer, primary_key = True, autoincrement = True)
    peso = db.Column(db.Integer)
    id_formulario = db.Column(db.Integer, db.ForeignKey('formulario.id_formulario'))
    id_materia = db.Column(db.Integer, db.ForeignKey('materia.id_materia'))

    formulario = db.relationship('Formulario', foreign_keys=id_formulario)
    materia = db.relationship('Materia', foreign_keys=id_materia)
    

    def __init__(self, peso, id_formulario, id_materia):
        self.peso = peso
        self.id_formulario = id_formulario
        self.id_materia = id_materia

    def __repr__(self):
        return "<Materia_peso {}>".format(self.peso)