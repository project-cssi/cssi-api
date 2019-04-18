from marshmallow import fields, validate
from .. import db, ma
from .application import ApplicationSchema
from .questionnaire import QuestionnaireSchema


class Session(db.Model):
    __tablename__ = 'session'

    id = db.Column(db.Integer, primary_key=True)
    app_id = db.Column(db.Integer, db.ForeignKey('application.id', use_alter=True, name='fk_app_id'), nullable=False)
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    expected_emotions = db.Column(db.JSON, nullable=False)
    questionnaire_id = db.Column(db.Integer, db.ForeignKey('questionnaire.id', use_alter=True, name='fk_questionnaire_id'), nullable=False)
    cssi_score = db.Column(db.Float, nullable=False, default=0)
    latency_scores = db.Column(db.JSON, nullable=False, default={})
    total_latency_score = db.Column(db.Float, nullable=False, default=0)
    sentiment_scores = db.Column(db.JSON, nullable=False, default={})
    total_sentiment_score = db.Column(db.Float, nullable=False, default=0)
    questionnaire_scores = db.Column(db.JSON, nullable=True, default={})
    total_questionnaire_score = db.Column(db.Float, nullable=False, default=0)

    def __init__(self, app, expected_emotions, questionnaire):
        self.app = app
        self.expected_emotions = expected_emotions
        self.questionnaire = questionnaire

    def __repr__(self):
        return '<Session %r>' % self.id


class SessionSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    creation_date = fields.DateTime(dump_only=True)
    expected_emotions = fields.List(fields.String(), required=True)
    app = fields.Nested(ApplicationSchema, dump_only=True)
    questionnaire = fields.Nested(QuestionnaireSchema, dump_only=True)
    cssi_score = fields.Float()
    latency_scores = fields.Dict()
    total_latency_score = fields.Float()
    sentiment_scores = fields.Dict()
    total_sentiment_score = fields.Float()
    questionnaire_scores = fields.Dict()
    total_questionnaire_score = fields.Float()

