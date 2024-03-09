#!/usr/bin/python
# -*- coding: utf-8 -*-

import flask
from flask import url_for
from app import app, db
from app.forms import LearnForm, AddWordForm, AddDataset
from app.models import User, DatasetInfo, Pair
from app.db_helpers import add_new_dataset

app.app_context().push()

# only one user for now
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
    global global_dataset_id
    form = LearnForm()
    if form.validate_on_submit():
        answer = form.answer.data
        return flask.redirect(url_for('learn', feedback="test"))

    return flask.render_template('learn.html', form=form, is_dataset_selected=1 if global_dataset_id else 0)


@app.route('/add_word', methods=['POST', 'GET'])
def add_word():
    global global_dataset_id
    form = AddWordForm()
    if form.validate_on_submit():
        question = form.question.data
        answer = form.answer.data

        return flask.redirect('/add_word')

    return flask.render_template('add_word.html', form=form, is_dataset_selected=1 if global_dataset_id else 0)


@app.route('/add_dataset', methods=['POST', 'GET'])
def add_dataset():
    global global_user_id
    form = AddDataset()
    if form.validate_on_submit():
        new = form.dataset_name.data
        ret = add_new_dataset(global_user_id, new)
        print(new, ret)
        return flask.render_template('add_dataset.html', feedback=ret, new_name=new, form=form)
    return flask.render_template('add_dataset.html', form=form, feedback=None, new_name=None)
