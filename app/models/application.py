from .. import db, ma


class Application(db.Model):
    __tablename__ = 'applications'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    genre = db.Column(db.String(250), nullable=False)

    def __init__(self, name, genre):
        self.name = name
        self.genre = genre


class ApplicationSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'creation_date', 'genre')
