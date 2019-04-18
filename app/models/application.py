from marshmallow import fields, validate
from .application_type import ApplicationTypeSchema
from .genre import GenreSchema
from .. import db, ma


class Application(db.Model):
    __tablename__ = 'application'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    identifier = db.Column(db.String(100), nullable=False)
    developer = db.Column(db.String(100), nullable=False)
    type_id = db.Column(db.Integer, db.ForeignKey('application_type.id', use_alter=True, name='fk_type_id'), nullable=False)
    description = db.Column(db.String(250), nullable=False)
    public_sharing = db.Column(db.Boolean, nullable=False, default=False)
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id', use_alter=True, name='fk_genre_id'), nullable=False)
    sessions = db.relationship('Session', backref='app', lazy='dynamic')

    def __init__(self, name, identifier, developer, type, description, genre):
        self.name = name
        self.identifier = identifier
        self.developer = developer
        self.type = type
        self.description = description
        self.genre = genre

    def __repr__(self):
        return '<Application %r>' % self.id


class ApplicationSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(1, 100))
    identifier = fields.String()
    developer = fields.String(required=True, validate=validate.Length(1, 100))
    type = fields.Nested(ApplicationTypeSchema, dump_only=True)
    description = fields.String(required=True, validate=validate.Length(1, 250))
    creation_date = fields.DateTime(dump_only=True)
    genre = fields.Nested(GenreSchema, dump_only=True)
    public_sharing = fields.Boolean(required=True)
