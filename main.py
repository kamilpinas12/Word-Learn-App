#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlalchemy as sa
import sqlalchemy.orm as so
from app import app, db
from app.models import User, DatasetInfo, Pair


@app.shell_context_processor
def make_shell_context():
    return {'sa': sa, 'so': so, 'db': db, 'User': User, 'Pair': Pair, 'DatasetInfo': DatasetInfo}

