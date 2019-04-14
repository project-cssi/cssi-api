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
    TYPE_META_FILE_PATH (str): Path for the file containing application type meta

Authors:
    Brion Mario

"""

import os
import json
from marshmallow import fields, validate
from .. import db, ma

GENRE_META_FILE_PATH = 'meta/genre.meta.json'


class Application(db.Model):
    __tablename__ = 'application'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type_id = db.Column(db.Integer, db.ForeignKey('application_type.id', ondelete='CASCADE'), nullable=False)
    type = db.relationship('Type', backref=db.backref('application', lazy='dynamic'))
    description = db.Column(db.String(250), nullable=False)
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id', ondelete='CASCADE'), nullable=False)
    genre = db.relationship('Genre', backref=db.backref('application', lazy='dynamic'))

    def __init__(self, name, description, genre_id):
        self.name = name
        self.description = description
        self.genre_id = genre_id

    def __repr__(self):
        return '<Application \'%s\'>' % self.name


class Genre(db.Model):
    __tablename__ = 'genre'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    @classmethod
    def seed(cls):
        if os.path.exists(GENRE_META_FILE_PATH):
            with open(GENRE_META_FILE_PATH) as genre_meta_json:
                data = json.load(genre_meta_json)
                for genre in data['genre']:
                    genre = Genre(name=genre['name'])
                    genre.save()
        else:
            # TODO: Add exception
            print("Couldn't locate meta file")

    def save(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return '<Genre \'%s\'>' % self.name


class Type(db.Model):
    __tablename__ = 'application_type'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<ApplicationType \'%s\'>' % self.name


class ApplicationSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(1, 100))
    type_id = fields.Integer(required=True)
    description = fields.String(required=True, validate=validate.Length(1, 250))
    creation_date = fields.DateTime()
    genre_id = fields.Integer(required=True)


class GenreSchema(ma.Schema):
    id = fields.Integer()
    name = fields.String(required=True)


class TypeSchema(ma.Schema):
    id = fields.Integer()
    name = fields.String(required=True)
