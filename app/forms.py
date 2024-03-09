#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class LearnForm(FlaskForm):
    answer = StringField('Answer', render_kw={'autofocus': True})
    submit = SubmitField('Submit')


class AddWordForm(FlaskForm):
    question = StringField('Question', validators=[DataRequired()])
    answer = StringField('Answer', validators=[DataRequired()])
    submit = SubmitField('Add')


class AddDataset(FlaskForm):
    dataset_name = StringField('Enter dataset name')
    submit = SubmitField('Submit')
