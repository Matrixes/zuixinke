# -*- coding:utf-8 -*-

from flask import render_template, flash, redirect, url_for, request
from flask.ext.login import login_required, current_user, login_user
from .. import db
from ..models import User
from . import main
from .forms import EditProfileForm
from ..auth.forms import LoginForm


@main.route('/',methods=['GET','POST'])
def index():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash(u'用户名或密码错误')
    is_index = True
    return render_template('index.html',form=form,is_index = is_index)


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    return render_template('user.html',user=user)


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        db.session.commit()
        flash(u'资料已更改')
        return redirect(url_for('main.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)