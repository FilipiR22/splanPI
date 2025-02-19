from utils import db

class Progresso(db.Model):
    __tablename__='progresso'
    id_progresso = db.Column(db.Integer, primary_key = True, autoincrement = True)
    concluido = db.Column(db.Integer)
    tempo_estudado = db.Column(db.Float)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    id_assunto = db.Column(db.Integer, db.ForeignKey('assunto.id_assunto'))

    usuario = db.relationship('Usuario', foreign_keys=id_usuario)
    assunto = db.relationship('Assunto', foreign_keys=id_assunto)
    

    def __init__(self, concluido, tempo_estudado, id_usuario, id_assunto):
        self.concluido = concluido
        self.tempo_estudado = tempo_estudado
        self.id_usuario = id_usuario
        self.id_assunto = id_assunto

    def __repr__(self):
        return "<Progresso {}>".format(self.concluido)
