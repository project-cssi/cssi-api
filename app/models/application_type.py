import os
import json
from marshmallow import fields, validate
from .. import db, ma

APPLICATION_TYPE_META_FILE_PATH = 'meta/application_type.meta.json'


class ApplicationType(db.Model):
    __tablename__ = 'application_type'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    display_name = db.Column(db.String(100), nullable=False)
    display_name_full = db.Column(db.String(250), nullable=False)
    applications = db.relationship('Application', backref='app_type', lazy='dynamic')

    @classmethod
    def seed(cls):
        if cls.is_table_empty(cls):
            if os.path.exists(APPLICATION_TYPE_META_FILE_PATH):
                with open(APPLICATION_TYPE_META_FILE_PATH) as app_type_meta_json:
                    data = json.load(app_type_meta_json)
                    for item in data['types']:
                        app_type = ApplicationType(name=item['name'], display_name=item['display_name'], display_name_full=item['display_name_full'])
                        app_type.save()
                        print("Adding application type metadata: {}".format(app_type))
            else:
                # TODO: Add exception
                print("Couldn't locate meta file")
        else:
            print('Table is already filled')

    def save(self):
        db.session.add(self)
        db.session.commit()

    def is_table_empty(self):
        if not self.query.all():
            return True
        return False

    def __repr__(self):
        return self.display_name_full


class ApplicationTypeSchema(ma.Schema):
    id = fields.Integer()
    name = fields.String(required=True)
    display_name = fields.String(required=True)
    display_name_full = fields.String(required=True)
