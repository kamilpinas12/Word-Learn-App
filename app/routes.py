#!/usr/bin/python
# -*- coding: utf-8 -*-
import flask
from flask import render_template
from app import app



@app.route('/')
@app.route('/index')
def index():
    return flask.render_template('base.html')