#!/usr/bin/python
# -*- coding: utf-8 -*-

import flask
from flask import render_template
from app import app
from app.forms import LearnForm, AddWordForm


@app.route('/')
def empty():
    return flask.render_template('base.html')


@app.route('/learn', methods=['POST', 'GET'])
def learn():
    form = LearnForm()
    if form.validate_on_submit():
        answer = form.answer.data
        print(answer)
        return flask.redirect('/learn')

    return flask.render_template('learn.html', form=form)


@app.route('/add_word', methods=['POST', 'GET'])
def add_word():
    form = AddWordForm()
    if form.validate_on_submit():
        return flask.redirect('/add_word')

    return flask.render_template('add_word.html', form=form)