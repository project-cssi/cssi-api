import os
import json
from marshmallow import fields
from .. import db, ma

GENRE_META_FILE_PATH = 'meta/genre.meta.json'


class Genre(db.Model):
    __tablename__ = 'genre'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    display_name = db.Column(db.String(250), nullable=False)
    applications = db.relationship('Application', backref='genre', lazy='dynamic')

    def __init__(self, name, display_name):
        self.name = name
        self.display_name = display_name

    @classmethod
    def seed(cls):
        if cls.is_table_empty(cls):
            if os.path.exists(GENRE_META_FILE_PATH):
                with open(GENRE_META_FILE_PATH) as genre_meta_json:
                    data = json.load(genre_meta_json)
                    for item in data['genre']:
                        genre = Genre(name=item['name'], display_name=item['display_name'])
                        genre.save()
                        print("Adding genre metadata: {}".format(genre))
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
        return '<Genre %r>' % self.id


class GenreSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    display_name = fields.String(required=True)
