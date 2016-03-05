from app import create_app, db
from app.models import User,  Post, Category
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand
from werkzeug.contrib.fixers import ProxyFix

app = create_app('default')
app.wsgi_app = ProxyFix(app.wsgi_app)
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, Post=Post, Category=Category)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
