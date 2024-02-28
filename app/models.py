#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from datetime import datetime


# class User(db.Model):
#     id: so.Mapped[int] = so.mapped_column(primary_key=True)
#
#
# class Dataset(db.Model):
#     id: so.Mapped[int] = so.mapped_column(primary_key=True)
#
#
# class DatasetStats(db.Model):
#     time_stamp: so.Mapped[datetime] = so.mapped_column(sa.String(15))
#     correct: so.Mapped[int] = so.mapped_column()
#     wrong: so.Mapped[int] = so.mapped_column()
#     user_id: so.Mapped[User] = so.mapped_column(sa.ForeignKey(User.id))
