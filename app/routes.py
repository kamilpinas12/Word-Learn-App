#!/usr/bin/python
# -*- coding: utf-8 -*-

import flask
from flask import url_for
from sqlalchemy import delete

from app import app, db
from app.forms import LearnForm, AddWordForm, AddDataset
from app.models import User, DatasetInfo, Pair
from app.db_helpers import add_new_dataset, add_word_to_dataset

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
        ret = add_word_to_dataset(global_dataset_id, question, answer)
        if ret == 1:
            return flask.redirect(url_for('add_word'))
        return flask.render_template('add_word.html', ret=ret, is_dataset_selected=1, form=form)

    return flask.render_template('add_word.html', form=form, is_dataset_selected=1 if global_dataset_id else 0, ret=None)


@app.route('/add_dataset', methods=['POST', 'GET'])
def add_dataset():
    global global_user_id
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
        # dc = {"Written words": 0, "Accuracy": 0, "Words in dataset": 0, "Word with worst accuracy": '', "Accuracy of "
        #                                                                                              "worst word": 0}
        # worst_accuracy = None
        # worst_accuracy_pair = None
        # correct = 0
        # words = 0
        # for pair in pairs:
        #     words += 1
        #     typed = pair.correct + pair.wrong
        #     dc["Written words"] += typed
        #     dc["Words in dataset"] += 1
        #     correct += pair.correct
        #     acc = pair.correct/typed
        #     if worst_accuracy is None or worst_accuracy > acc:
        #         worst_accuracy_pair = acc
        #         worst_accuracy = pair
        # dc["Accuracy"] = correct / dc["Written words"]
        # dc["Word with worst accuracy"] = worst_accuracy_pair.answer
        # dc["Word with worst accuracy"] = worst_accuracy

        return flask.render_template('/stats.html', is_dataset_selected=1, pairs=pairs)