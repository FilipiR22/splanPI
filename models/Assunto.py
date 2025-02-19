from utils import db

class Assunto(db.Model):
    __tablename__='assunto'
    id_assunto = db.Column(db.Integer, primary_key = True, autoincrement = True)
    nome = db.Column(db.String(150))
    duracao = db.Column(db.Float)
    id_materia = db.Column(db.Integer, db.ForeignKey('materia.id_materia'))
    
    materia = db.relationship('Materia', foreign_keys=id_materia)


    def __init__(self, nome, duracao, id_materia):
        self.nome = nome
        self.duracao = duracao
        self.id_materia = id_materia

    def __repr__(self):
        return "<Assunto {}>".format(self.nome)
