from marshmallow import fields, validate
from .. import db, ma


class Application(db.Model):
    __tablename__ = 'application'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    identifier = db.Column(db.String(100), nullable=False)
    developer = db.Column(db.String(100), nullable=False)
    type_id = db.Column(db.Integer, db.ForeignKey('application_type.id', use_alter=True, name='fk_type_id'), nullable=False)
    description = db.Column(db.String(250), nullable=False)
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id', use_alter=True, name='fk_genre_id'), nullable=False)
    sessions = db.relationship('Session', backref='application', lazy='dynamic')

    def __repr__(self):
        return self.name


class ApplicationSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(1, 100))
    identifier = fields.String()
    developer = fields.String(required=True, validate=validate.Length(1, 100))
    type = fields.String(required=True)
    description = fields.String(required=True, validate=validate.Length(1, 250))
    creation_date = fields.DateTime()
    genre = fields.String(required=True)
