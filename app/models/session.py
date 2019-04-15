from marshmallow import fields, validate
from .. import db, ma


class Session(db.Model):
    __tablename__ = 'session'

    id = db.Column(db.Integer, primary_key=True)
    app_id = db.Column(db.Integer, db.ForeignKey('application.id', use_alter=True, name='fk_app_id'), nullable=False)
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    expected_emotions = db.Column(db.String, nullable=False)
    cssi_score = db.Column(db.Float, nullable=False, default=0)
    latency_scores = db.Column(db.String, nullable=False, default={})
    total_latency_score = db.Column(db.Float, nullable=False, default=0)
    sentiment_scores = db.Column(db.String, nullable=False, default={})
    total_sentiment_score = db.Column(db.Float, nullable=False, default=0)
    questionnaire_id = db.Column(db.Integer, db.ForeignKey('questionnaire.id', use_alter=True, name='fk_questionnaire_id'), nullable=False)
    questionnaire = db.relationship('Questionnaire', backref='session', lazy='dynamic')
    questionnaire_scores = db.Column(db.String, nullable=True, default={})
    total_questionnaire_score = db.Column(db.Float, nullable=False, default=0)

    def __repr__(self):
        return self.name


class SessionSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    creation_date = fields.DateTime()
    expected_emotions = fields.String(required=True)
