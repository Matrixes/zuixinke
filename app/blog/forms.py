#-*- coding:utf-8 -*-

from flask.ext.wtf import Form
from flask.ext.pagedown.fields import PageDownField
from wtforms import StringField, TextAreaField,SelectField, SubmitField
from wtforms.validators import Required

class PostForm(Form):
    title = StringField(u'标题',validators=[Required()])

    tag = StringField(u'标签',validators=[Required()])

    summary = PageDownField(u'摘要',validators=[Required()])
    body = PageDownField(u'内容',validators=[Required()])
    submit = SubmitField(u'发表')