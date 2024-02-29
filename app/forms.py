#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
class TestForm(FlaskForm):
    answer = StringField('Answer')
    submit = SubmitField('Submit')


class AddWordForm(FlaskForm):
    question = StringField('Question', validators=[DataRequired()])
    answer = StringField('Answer', validators=[DataRequired()])
