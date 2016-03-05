# -*- coding:utf-8 -*-

from flask import render_template, url_for, request, flash, request, abort
from flask.ext.login import login_required, current_user
from . import about


@about.route('/')
def index():
    return render_template('about/index.html')


@about.route('/resume')
@login_required
def resume():
    if not current_user.is_authenticated:
        about(403)
    return render_template('about/resume_2.html')