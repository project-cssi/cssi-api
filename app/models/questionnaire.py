from marshmallow import fields, validate
from .. import db, ma


class Questionnaire(db.Model):
    __tablename__ = 'questionnaire'

    id = db.Column(db.Integer, primary_key=True)
    pre = db.Column(db.JSON, nullable=False)
    post = db.Column(db.JSON, nullable=False, default={})
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    session = db.relationship("Session", uselist=False, backref="questionnaire")

    def __init__(self, pre, post):
        self.pre = pre
        self.post = post

    def __repr__(self):
        return '<Questionnaire %r>' % self.id


class SymptomSchema(ma.Schema):
    name = fields.String(required=False)
    display_name = fields.String(required=False)
    score = fields.String(required=False)


class QuestionnaireSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    pre = fields.List(fields.Nested(SymptomSchema), dump_only=True)
    post = fields.List(fields.Nested(SymptomSchema), dump_only=True)
    creation_date = fields.DateTime()
