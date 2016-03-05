from flask import render_template
from . import main
from ..auth import auth
from ..blog import blog


@main.app_errorhandler(403)
@auth.app_errorhandler(403)
@blog.app_errorhandler(403)
def forbidden(e):
    return render_template('errors/403.html'), 403


@main.app_errorhandler(404)
@auth.app_errorhandler(404)
@blog.app_errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404


@main.app_errorhandler(500)
@auth.app_errorhandler(500)
@blog.app_errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html'), 500
