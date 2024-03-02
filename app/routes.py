#!/usr/bin/python
# -*- coding: utf-8 -*-
import flask
from flask import render_template
from app import app
from app.forms import LearnForm, AddWordForm



@app.route('/')
@app.route('/learn', methods=['POST', 'GET'])
def learn():
    form = LearnForm()
    return flask.render_template('learn.html', form=form)


@app.route('/add_word', methods=['POST', 'GET'])
def add_word():
    form = AddWordForm()
    return flask.render_template('add_word.html', form=form)