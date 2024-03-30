#!/usr/bin/python
# -*- coding: utf-8 -*-

import flask
from flask import url_for

from app import app, db
from app.forms import LearnForm, AddWordForm, AddDataset
from app.models import User, DatasetInfo, Pair
from app.db_helpers import add_new_dataset, add_word_to_dataset, update_stats

app.app_context().push()

# only one user for now
global_user_id = 1
global_dataset_id = None


@app.route('/')
def select_dataset():
    global global_user_id
    global global_dataset_id
    datasets = db.session.query(DatasetInfo).join(User).filter(User.id == global_user_id).all()
    return flask.render_template('select_dataset.html', datasets=datasets, current_dataset_id=global_dataset_id)


@app.route('/set_dataset/<int:id>')
def set_dataset(id):
    global global_dataset_id
    global_dataset_id = id
    return flask.redirect('/')


selected_word = None


@app.route('/learn', methods=['POST', 'GET'])
def learn():
    global global_dataset_id
    global selected_word
    form = LearnForm()
    if form.validate_on_submit():
        answer = form.answer.data
        if selected_word:
            if selected_word.answer == answer:
                update_stats(selected_word.id, True, global_dataset_id)
                return flask.redirect(url_for('learn'))
            else:
                update_stats(selected_word.id, False, global_dataset_id)
                return flask.redirect(url_for('wrong_word'))

        return flask.redirect(url_for('learn'))
    else:
        selected_word = db.session.query(Pair). \
            filter_by(dataset_id=global_dataset_id).order_by(Pair.factor.desc()).first()

    return flask.render_template('learn.html', form=form, is_dataset_selected=1 if global_dataset_id else 0,
                                 question=selected_word)


@app.route('/wrong_word', methods=['POST', 'GET'])
def wrong_word():
    global selected_word
    form = LearnForm()
    if form.validate_on_submit():
        answer = form.answer.data
        if selected_word and answer == selected_word.answer:
            return flask.redirect(flask.url_for('learn'))
        else:
            return flask.redirect(flask.url_for('wrong_word'))
    else:
        return flask.render_template('/wrong_word.html', form=form, question=selected_word)


@app.route('/add_word', methods=['POST', 'GET'])
def add_word():
    global global_dataset_id
    form = AddWordForm()
    if form.validate_on_submit():
        question = form.question.data
        answer = form.answer.data
        ret = add_word_to_dataset(global_dataset_id, question, answer)
        if ret == 1:
            return flask.redirect(url_for('add_word'))
        return flask.render_template('add_word.html', ret=ret, is_dataset_selected=1, form=form)

    return flask.render_template('add_word.html', form=form, is_dataset_selected=1 if global_dataset_id else 0,
                                 ret=None)


@app.route('/add_dataset', methods=['POST', 'GET'])
def add_dataset():
    global global_user_id
    global global_dataset_id
    form = AddDataset()
    if form.validate_on_submit():
        new = form.dataset_name.data
        ret = add_new_dataset(global_user_id, new)
        if ret == 1:
            return flask.redirect(url_for('add_dataset'))
        return flask.render_template('add_dataset.html', feedback=ret, new_name=new)
    return flask.render_template('add_dataset.html', form=form, feedback=None, new_name=None)


@app.route('/delete_dataset/<int:id>')
def delete_dataset(id):
    global global_dataset_id
    if id == global_dataset_id:
        global_dataset_id = None

    DatasetInfo.query.filter_by(id=id).delete()
    Pair.query.filter_by(dataset_id=id).delete()
    db.session.commit()

    return flask.redirect('/')


@app.route('/stats', methods=['POST', 'GET'])
def stats():
    global global_dataset_id
    if global_dataset_id is None:
        return flask.render_template('stats.html', is_dataset_selected=0)
    else:
        pairs = db.session.query(Pair).join(DatasetInfo).filter(DatasetInfo.id == global_dataset_id).all()

        correct = 0
        wrong = 0
        for pair in pairs:
            correct += pair.correct
            wrong += pair.wrong
        word_typed = correct + wrong
        if word_typed > 0:
            accuracy = 100 * correct // word_typed
        else:
            accuracy = -1

        return flask.render_template('/stats.html', is_dataset_selected=1, pairs=pairs, accuracy=accuracy, word_typed=word_typed)


@app.route('/delete_word/<int:id>')
def delete_word(id):
    global global_dataset_id

    Pair.query.filter_by(id=id).delete()
    db.session.commit()

    return flask.redirect(url_for('stats'))