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


class ApplicationSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(1, 100))
    app_type = fields.String(required=True)
    description = fields.String(required=True, validate=validate.Length(1, 250))
    creation_date = fields.DateTime()
    genre = fields.String(required=True)
