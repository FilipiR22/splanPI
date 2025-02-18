from utils import db

class Conteudo(db.Model):
    __tablename__='conteudo'
    id_conteudo = db.Column(db.Integer, primary_key = True, autoincrement = True)
    nome = db.Column(db.String(150))
    id_assunto = db.Column(db.Integer, db.ForeignKey('assunto.id_assunto'))

    assunto = db.relationship('Assunto', foreign_keys=id_assunto)


    def __init__(self, nome, id_assunto):
        self.nome = nome
        self.id_assunto = id_assunto

    def __repr__(self):
        return "<Conteudo {}>".format(self.nome)