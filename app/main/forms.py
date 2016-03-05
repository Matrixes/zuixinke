#-*- coding:utf-8 -*-

from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import Length


class EditProfileForm(Form):
    name = StringField(u'您的名字', validators=[Length(0, 64)])
    location = StringField(u'居住地', validators=[Length(0, 64)])
    about_me = TextAreaField(u'介绍')
    submit = SubmitField(u'提交')

