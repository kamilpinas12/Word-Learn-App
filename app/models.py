#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from datetime import datetime


class User(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    dataset: so.WriteOnlyMapped['DatasetsList'] = so.relationship(
        back_populates='author')

    def __repr__(self):
        return f'User {self.username}'


class DatasetsList(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(30), index=True, unique=True)
    dataset: so.WriteOnlyMapped['Dataset'] = so.relationship(
        back_populates='dataset_name')
    author: so.Mapped[User] = so.relationship(back_populates='dataset')
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)

    def __repr__(self):
        return f'Dataset: {self.name}'


class Dataset(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    question: so.Mapped[str] = so.mapped_column(sa.String(150), index=True, unique=True)
    answer: so.Mapped[str] = so.mapped_column(sa.String(30), index=True, unique=True)
    factor: so.Mapped[float] = so.mapped_column(index=True)
    correct: so.Mapped[int] = so.mapped_column(index=True)
    wrong: so.Mapped[float] = so.mapped_column(index=True)
    lst_apperance: so.Mapped[int] = so.mapped_column(index=True)
    dataset_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(DatasetsList.id),
                                                  index=True)
    dataset_name: so.Mapped[DatasetsList] = so.relationship(
        back_populates='dataset')














