#!/usr/bin/python
# -*- coding: utf-8 -*-

import flask
from flask import render_template
from app import app, db
from app.forms import LearnForm, AddWordForm, AddDataset
from app.models import User, DatasetInfo, Pair
import sqlalchemy as sa


app.app_context().push()

#only one user for now
global_user_id = 1
global_dataset_id = None

@app.route('/')
def select_dataset():
    global global_user_id
    datasets = db.session.query(DatasetInfo).join(User).filter(User.id == global_user_id).all()
    return flask.render_template('select_dataset.html', datasets=datasets)


@app.route('/set_dataset/<int:id>')
def set_dataset(id):
    global global_dataset_id
    global_dataset_id = id
    return flask.redirect('/')


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
        question = form.question.data
        answer = form.answer.data
        print(question, answer)
        return flask.redirect('/add_word')

    return flask.render_template('add_word.html', form=form)


@app.route('/add_dataset', methods=['POST', 'GET'])
def add_dataset():
    form = AddDataset()
    if form.validate_on_submit():
        return flask.redirect('/add_dataset')
    return flask.render_template('add_dataset.html', form=form)

