from flask import render_template
from . import bbs


@bbs.route('/')
def index():
    return render_template('bbs/index.html')