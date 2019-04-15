from marshmallow import fields, validate
from .. import db, ma


class Questionnaire(db.Model):
    __tablename__ = 'questionnaire'

    id = db.Column(db.Integer, primary_key=True)
    pre = db.Column(db.String, nullable=False)
    post = db.Column(db.String, nullable=False)
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    session_id = db.Column(db.Integer, db.ForeignKey('session.id', use_alter=True, name='fk_session_id'), nullable=False)
    session = db.relationship('Session', backref='questionnaire', lazy='dynamic')

    def __repr__(self):
        return self.id


class ApplicationSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    pre = fields.String(required=True, validate=validate.Length(1))
    post = fields.String(required=False)
    creation_date = fields.DateTime()
