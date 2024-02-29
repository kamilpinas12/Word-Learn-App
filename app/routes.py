#!/usr/bin/python
# -*- coding: utf-8 -*-
import flask
from flask import render_template
from app import app
from app.forms import TestForm, AddWordForm



@app.route('/')
@app.route('/test', methods=['POST', 'GET'])
def test():
    form = TestForm()
    return flask.render_template('test.html', form=form)


@app.route('/add_word', methods=['POST', 'GET'])
def add_word():
    form = AddWordForm()
    return flask.render_template('add_word.html', form=form)