#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db


class User(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    dataset: so.WriteOnlyMapped['DatasetInfo'] = so.relationship(
        back_populates='author', cascade='all, delete, delete-orphan')

    def __repr__(self):
        return f'User {self.username}'


class DatasetInfo(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(30), index=True, unique=True)

    author: so.Mapped[User] = so.relationship(back_populates='dataset')
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)

    pair: so.WriteOnlyMapped['Pair'] = so.relationship(
        back_populates='dataset_info', cascade='all, delete, delete-orphan')

    def __repr__(self):
        return f'Dataset: {self.name}'


class Pair(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    question: so.Mapped[str] = so.mapped_column(sa.String(150), index=True, unique=True)
    answer: so.Mapped[str] = so.mapped_column(sa.String(30), index=True, unique=True)
    factor: so.Mapped[float] = so.mapped_column(index=True)
    correct: so.Mapped[int] = so.mapped_column(index=True)
    wrong: so.Mapped[float] = so.mapped_column(index=True)

    dataset_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(DatasetInfo.id),
                                                  index=True)
    dataset_info: so.Mapped[DatasetInfo] = so.relationship(
        back_populates='pair')

    def __repr__(self):
        return f'{self.question} : {self.answer}'












