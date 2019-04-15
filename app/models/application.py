#!/usr/bin/env python
# -*- coding: utf-8 -*-

# (c) Copyright 2019 Brion Mario.
# (c) This file is part of the CSSI REST API and is made available under MIT license.
# (c) For more information, see https://github.com/brionmario/cssi-api/blob/master/LICENSE.txt
# (c) Please forward any queries to the given email address. email: brion@apareciumlabs.com

"""Models and Schemas for Applications

This module handles contains the different db models and schemas
for applications.

Attributes:
    GENRE_META_FILE_PATH (str): Path for the file containing genre meta
    APPLICATION_TYPE_META_FILE_PATH (str): Path for the file containing application type meta

Authors:
    Brion Mario

"""

import os
import json
from marshmallow import fields, validate
from .. import db, ma

GENRE_META_FILE_PATH = 'meta/genre.meta.json'
APPLICATION_TYPE_META_FILE_PATH = 'meta/application_type.meta.json'


class Application(db.Model):
    __tablename__ = 'application'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    app_type_id = db.Column(db.Integer, db.ForeignKey('application_type.id', use_alter=True, name='fk_app_type_id'), nullable=False)
    description = db.Column(db.String(250), nullable=False)
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id', use_alter=True, name='fk_genre_id'), nullable=False)

    def __repr__(self):
        return self.name


class Genre(db.Model):
    __tablename__ = 'genre'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    display_name = db.Column(db.String(250), nullable=False)
    applications = db.relationship('Application', backref='genre', lazy='dynamic')

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
        return self.display_name


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


class ApplicationSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(1, 100))
    app_type = fields.String(required=True)
    description = fields.String(required=True, validate=validate.Length(1, 250))
    creation_date = fields.DateTime()
    genre = fields.String(required=True)


class GenreSchema(ma.Schema):
    id = fields.Integer()
    name = fields.String(required=True)
    display_name = fields.String(required=True)


class ApplicationTypeSchema(ma.Schema):
    id = fields.Integer()
    name = fields.String(required=True)
    display_name = fields.String(required=True)
    display_name_full = fields.String(required=True)
