from marshmallow import fields, validate
from .. import db, ma


class Application(db.Model):
    __tablename__ = 'application'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id', ondelete='CASCADE'), nullable=False)
    genre = db.relationship('Genre', backref=db.backref('application', lazy='dynamic'))

    def __init__(self, name, genre):
        self.name = name
        self.genre = genre

    def __repr__(self):
        return '<Application \'%s\'>' % self.name


class Genre(db.model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)


class ApplicationSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(1))
    creation_date = fields.DateTime()
    genre_id = fields.Integer(required=True)


class GenreSchema(ma.Schema):
    id = fields.Integer()
    name = fields.String(required=True)
