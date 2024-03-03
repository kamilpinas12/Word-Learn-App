#!/usr/bin/python
# -*- coding: utf-8 -*-

from app import db
from app.models import User, DatasetInfo, Pair


def add_pair_to_database(database: DatasetInfo, question: str, answer: str):
    new_pair = Pair(database)
    db.session.add()



